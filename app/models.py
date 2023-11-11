from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship

# base tunnel and block models for CRUD


class TargetLink(SQLModel, table=True):
    source_id: int = Field(foreign_key="tunnel.id", primary_key=True)
    target_id: int = Field(foreign_key="block.id", primary_key=True)


class TunnelBase(SQLModel):
    name: str = Field(default="My Tunnel", index=True)


class Tunnel(TunnelBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    blocks: List["Block"] = Relationship(back_populates="tunnel")
    targets: List["Block"] = Relationship(
        back_populates="sources",
        sa_relationship_kwargs={
            "secondary": "targetlink",
            "primaryjoin": "Tunnel.id == TargetLink.source_id",
            "secondaryjoin": "Block.id == TargetLink.target_id",
        },
    )


class TunnelCreate(TunnelBase):
    pass


class TunnelRead(TunnelBase):
    id: int


class TunnelUpdate(SQLModel):
    name: Optional[str] = None


# A block can only have one tunnel: one-to-one relationship
class BlockBase(SQLModel):
    name: str = Field(default=None, index=True)
    block_type: str
    target_tunnel_out: bool = Field(default=False)
    # Note: tunnel_id is moved to Block as it needs to reference the table=True model


class Block(BlockBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tunnel: Optional["Tunnel"] = Relationship(back_populates="blocks")
    targets: List["Block"] = Relationship(
        back_populates="sources",
        sa_relationship_kwargs={
            "secondary": "targetlink",
            "primaryjoin": "Block.id == TargetLink.source_id",
            "secondaryjoin": "Block.id == TargetLink.target_id",
        },
    )
    sources: List["Tunnel"] = Relationship(
        back_populates="targets",
        sa_relationship_kwargs={
            "secondary": "targetlink",
            "primaryjoin": "Block.id == TargetLink.target_id",
            "secondaryjoin": "Tunnel.id == TargetLink.source_id",
        },
    )


class BlockCreate(BlockBase):
    pass


class BlockRead(BlockBase):
    id: int


class BlockUpdate(SQLModel):
    name: Optional[str] = None
    block_type: Optional[str] = None


# A tunnel can 'contain' many blocks: one-to-many relationship
class TunnelReadWithBlocks(TunnelRead):
    blocks: Optional[List[BlockRead]] = None


class BlockReadWithTargets(BlockRead):
    targets: Optional[List[BlockRead]] = None


# TunnelReadWithTargets should include a list of targets in addition to blocks
class TunnelReadWithTargets(TunnelRead):
    targets: Optional[List[BlockRead]] = None
