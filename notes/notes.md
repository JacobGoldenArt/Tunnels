```python
from fastapi import FastAPI
from pydantic import BaseModel
from .tunnel.operations import TunnelOps

app = FastAPI()

class Tunnel(BaseModel):
    name: str

@app.post("/tunnels", response_model=Tunnel)
def create_tunnel(tunnel: Tunnel):
    tunnel_id = TunnelOps.newTunnel(tunnel.name)
    return {"id": tunnel_id}

@app.put("/tunnels/{tunnel_id}")
def update_tunnel(tunnel_id: str, tunnel: Tunnel):
    TunnelOps.editTunnel(tunnel_id, tunnel.name)
    return {"message": f"Tunnel {tunnel_id} has been updated"}

@app.delete("/tunnels/{tunnel_id}")
def delete_tunnel(tunnel_id: str):
    TunnelOps.deleteTunnel(tunnel_id)
    return {"message": f"Tunnel {tunnel_id} has been deleted"}

class TunnelOps(Tunnel):
    tunnels = {}

    def __init__(self, name):
        super().__init__(name)
        self.__class__.tunnels[self.id] = self

    @classmethod
    def newTunnel(cls, name) -> str:
        """Create a new tunnel and return its ID"""
        tunnel_new = Tunnel(name)
        cls.tunnels[tunnel_new.id] = tunnel_new
        return str(tunnel_new.id)

    @classmethod
    def editTunnel(cls, tunnel_id, new_name):
        """Edit a tunnel's name"""
        tunnel = cls.tunnels[tunnel_id]
        tunnel.name = new_name

    @classmethod
    def deleteTunnel(cls, tunnel_id) -> None:
        """Delete a tunnel"""
        del cls.tunnels[tunnel_id]
```

