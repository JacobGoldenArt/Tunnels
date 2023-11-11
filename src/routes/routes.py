from typing import Dict, Any
from dataclasses import dataclass, field


@dataclass
class Routing:
    """
    Handles the routing between blocks.
    """

    routes: Dict[str, Any] = field(default_factory=dict)

    def add_route(self, source_block_name: str, target_block_name: str) -> None:
        """
        Add a route from source_block_name to target_block_name.
        """
        self.routes.setdefault(source_block_name, []).append(target_block_name)

    def remove_route(self, source_block_name: str, target_block_name: str) -> None:
        """
        Remove a route from source_block_name to target_block_name.
        """
        if target_block_name in self.routes.get(source_block_name, []):
            self.routes[source_block_name].remove(target_block_name)

    def get_targets(self, block_name: str) -> list:
        """
        Get the targets for the given block.
        """
        return self.routes.get(block_name, [])
    
    def model_dump(self) -> Dict[str, Any]:
        return {
            "routes": self.routes,
        }
