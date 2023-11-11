from typing import List
from models import (
    Block,
    BlockCreate,
    BlockRead,
    BlockUpdate,
    BlockReadWithTargets,
    TargetLink,
    Tunnel,
    TunnelCreate,
    TunnelRead,
    TunnelReadWithBlocks,
    TunnelReadWithTargets,
    TunnelUpdate,
)
from db_setup import get_session, create_db_and_tables, Session
from sqlmodel import select

from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/blocks/", response_model=BlockRead)
def create_block(*, session: Session = Depends(get_session), block: BlockCreate):
    db_block = Block.from_orm(block)
    session.add(db_block)
    session.commit()
    session.refresh(db_block)
    return db_block


@app.post("/blocks/{block_id}/targets/", response_model=List[BlockReadWithTargets])
def set_block_targets(
    block_id: int, target_ids: List[int], session: Session = Depends(get_session)
):
    db_block = session.get(Block, block_id)
    if not db_block:
        raise HTTPException(status_code=404, detail="Block not found")

    # Check if any of the target_ids is to target tunnel_out
    for target_id in target_ids:
        if target_id == block_id:
            continue  # Avoid a block targeting itself
        if target_id == -1:  # Assuming -1 is the indicator for tunnel_out
            db_block.target_tunnel_out = True
            session.add(db_block)
            continue
        target_link = TargetLink(source_id=block_id, target_id=target_id)
        session.add(target_link)

    session.commit()
    return [
        session.get(Block, target_id) for target_id in target_ids if target_id != -1
    ]  # Exclude tunnel_out indicator


@app.get("/blocks/", response_model=List[BlockRead])
def read_blocks(*, session: Session = Depends(get_session)):
    blocks = session.exec(select(Block)).all()
    return blocks


@app.get("/blocks/{block_id}", response_model=BlockReadWithTargets)
def read_block(*, session: Session = Depends(get_session), block_id: int):
    block = session.get(Block, block_id)
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")
    return block


@app.patch("/blocks/{block_id}", response_model=BlockReadWithTargets)
def update_block(
    *, session: Session = Depends(get_session), block_id: int, block: BlockUpdate
):
    db_block = session.get(Block, block_id)
    if not db_block:
        raise HTTPException(status_code=404, detail="Block not found")
    block_data = block.dict(exclude_unset=True)
    for key, value in block_data.items():
        setattr(db_block, key, value)
    session.add(db_block)
    session.commit()
    session.refresh(db_block)
    return db_block


@app.delete("/blocks/{block_id}")
def delete_block(*, session: Session = Depends(get_session), block_id: int):
    block = session.get(Block, block_id)
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")
    session.delete(block)
    session.commit()
    return {"message": "Block deleted"}


@app.post("/tunnels/", response_model=TunnelRead)
def create_tunnel(*, session: Session = Depends(get_session), tunnel: TunnelCreate):
    db_tunnel = Tunnel.from_orm(tunnel)
    session.add(db_tunnel)
    session.commit()
    session.refresh(db_tunnel)
    return db_tunnel


@app.post("/tunnels/{tunnel_id}/targets/", response_model=TunnelReadWithTargets)
def set_tunnel_targets(
    tunnel_id: int, target_ids: List[int], session: Session = Depends(get_session)
):
    db_tunnel = session.get(Tunnel, tunnel_id)
    if not db_tunnel:
        raise HTTPException(status_code=404, detail="Tunnel not found")

    # Fetch the target blocks
    target_blocks = session.exec(select(Block).where(Block.id.in_(target_ids))).all()
    if not target_blocks:
        raise HTTPException(status_code=404, detail="Target Block(s) not found")

    # Clear previous targets and set new ones
    db_tunnel.targets = target_blocks

    session.commit()
    return db_tunnel


@app.get("/tunnels/{tunnel_id}", response_model=TunnelReadWithBlocks)
def read_tunnel_blocks(*, tunnel_id: int, session: Session = Depends(get_session)):
    tunnel = session.get(Tunnel, tunnel_id)
    if not tunnel:
        raise HTTPException(status_code=404, detail="Tunnel not found")
    return tunnel


@app.get("/tunnels/{tunnel_id}", response_model=TunnelReadWithTargets)
def read_tunnel_targets(*, tunnel_id: int, session: Session = Depends(get_session)):
    tunnel = session.get(Tunnel, tunnel_id)
    if not tunnel:
        raise HTTPException(status_code=404, detail="Tunnel not found")
    return tunnel


@app.patch("/tunnels/{tunnel_id}", response_model=TunnelReadWithTargets)
def update_tunnel(
    *, session: Session = Depends(get_session), tunnel_id: int, tunnel: TunnelUpdate
):
    db_tunnel = session.get(Tunnel, tunnel_id)
    if not db_tunnel:
        raise HTTPException(status_code=404, detail="Tunnel not found")

    # Update tunnel with new data, excluding unset fields
    tunnel_data = tunnel.dict(exclude_unset=True)
    for key, value in tunnel_data.items():
        setattr(db_tunnel, key, value)

    session.commit()
    session.refresh(db_tunnel)
    return db_tunnel


@app.delete("/tunnels/{tunnel_id}")
def delete_tunnel(*, session: Session = Depends(get_session), tunnel_id: int):
    tunnel = session.get(Tunnel, tunnel_id)
    if not tunnel:
        raise HTTPException(status_code=404, detail="Tunnel not found")
    session.delete(tunnel)
    session.commit()
