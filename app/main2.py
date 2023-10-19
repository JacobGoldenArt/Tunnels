from tunnel.operations import TunnelOps
from blocks.operations import BlocksOps


# print(TunnelOps.tunnels)
#results = TunnelOps.newTunnel("bTunnel")
# print(results)  
results = BlocksOps.editBlock("653154165154b5772a1f8aa7", {
    "name": "sprinkles",
})

#results = BlocksOps.newBlock("donut", "textgen", "653153305b576844741564a3")
print(results)