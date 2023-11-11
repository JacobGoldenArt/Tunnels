from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship

# base tunnel and block models for CRUD


class TunnelBase(SQLModel):
    name: str = Field(default="My Tunnel", index=True)


class Tunnel(TunnelBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    blocks: List["Block"] = Relationship(back_populates="tunnel")


class TunnelCreate(TunnelBase):
    pass


class TunnelRead(TunnelBase):
    id: int


class TunnelUpdate(SQLModel):
    name: Optional[str] = None
    # blocks: Optional[List["Block"]] = None


class TargetLink(SQLModel, table=True):
    source_id: int = Field(primary_key=True, foreign_key="block.id")
    target_id: int = Field(primary_key=True, foreign_key="block.id")


# A block can only have one tunnel: one-to-one relationship
class BlockBase(SQLModel):
    name: str = Field(default=None, index=True)
    block_type: str
    tunnel_id: Optional[int] = Field(default=None, foreign_key="tunnel.id")
    target_tunnel_out: bool = Field(default=False)


class Block(BlockBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tunnel: Optional["Tunnel"] = Relationship(back_populates="blocks")
    targets: List["Block"] = Relationship(
        back_populates="sources", link_model=TargetLink
    )
    sources: List["Block"] = Relationship(back_populates="targets")


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


# Todo: Figure out how to model the following relationships:
# 1 Tunnle_Input can target one or more blocks (one-to-many relationship)
# 2. Many Blocks can target a single Block: many-to-one relationship
# 3. A block can have many (target) blocks: one-to-many relationship
# 4. Many Blocks can target one Tunnel_Output: many-to-one relationship
