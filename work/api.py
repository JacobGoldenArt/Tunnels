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


# Endpoint to set targets for a block


@app.post("/blocks/{block_id}/targets/", response_model=List[Block])
def set_block_targets(
    block_id: int, target_ids: List[int], session: Session = Depends(get_session)
):
    db_block = session.get(Block, block_id)
    if not db_block:
        raise HTTPException(status_code=404, detail="Block not found")

    # Add the target links
    for target_id in target_ids:
        if target_id == block_id:
            continue  # Avoid a block targeting itself
        target_link = TargetLink(source_id=block_id, target_id=target_id)
        session.add(target_link)

    session.commit()
    return [session.get(Block, target_id) for target_id in target_ids]


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


@app.patch("/blocks/{block_id}", response_model=BlockRead)
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


@app.get("/tunnels/{tunnel_id}", response_model=TunnelReadWithBlocks)
def read_tunnel(*, tunnel_id: int, session: Session = Depends(get_session)):
    tunnel = session.get(Tunnel, tunnel_id)
    if not tunnel:
        raise HTTPException(status_code=404, detail="Tunnel not found")
    return tunnel


@app.patch("/tunnels/{tunnel_id}", response_model=TunnelReadWithBlocks)
def update_tunnel(
    *, session: Session = Depends(get_session), tunnel_id: int, tunnel: TunnelUpdate
):
    # read a single tunnel from db
    db_tunnel = session.get(Tunnel, tunnel_id)
    if not db_tunnel:
        raise HTTPException(status_code=404, detail="Tunnel not found")
    # use exclude_unset=True to avoid overwriting existing values.
    tunnel_data = tunnel.dict(exclude_unset=True)
    # loop through the key/value pairs in tunnel_data
    # and update the corresponding attribute of db_tunnel
    for key, value in tunnel_data.items():
        setattr(db_tunnel, key, value)
    session.add(db_tunnel)
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
    return {"message": "Tunnel deleted"}


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=8000)
