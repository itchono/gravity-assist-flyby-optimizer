from .celestial_body import CelestialObject

class RelationalTreeNode:
    def __init__(self) -> None:
        self.parent: RelationalTreeNode = None
        self.children: list[RelationalTreeNode] = []
        self.data: CelestialObject = None

class RelationalTree:
    def __init__(self) -> None:
        self.root: RelationalTreeNode = RelationalTreeNode()