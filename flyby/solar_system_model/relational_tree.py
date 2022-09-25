from .celestial_body import CelestialBody


class RelationalTreeNode:
    def __init__(self) -> None:
        self.parent: RelationalTreeNode = None
        self.children: list[RelationalTreeNode] = []
        self.data: CelestialBody = None


class RelationalTree:
    def __init__(self) -> None:
        self.root: RelationalTreeNode = RelationalTreeNode()

    @classmethod
    def solar_system(cls):
        tree = cls()
        tree.root.data = CelestialBody.sun()
        tree.root.children = [RelationalTreeNode() for i in range(8)]
        tree.root.children[0].data = CelestialBody.mercury()
        tree.root.children[1].data = CelestialBody.venus()
        tree.root.children[2].data = CelestialBody.earth()
        tree.root.children[3].data = CelestialBody.mars()
        tree.root.children[4].data = CelestialBody.jupiter()
        tree.root.children[5].data = CelestialBody.saturn()
        tree.root.children[6].data = CelestialBody.uranus()
        tree.root.children[7].data = CelestialBody.neptune()

        for i in range(8):
            tree.root.children[i].parent = tree.root

        return tree
