from .celestial_body import CelestialBody


class RelationalTreeNode(CelestialBody):
    def __init__(self, body: CelestialBody) -> None:
        super().__init__(body.name, body.radius, body.mass, body.color, body.ephemeris_id)
        self.parent: RelationalTreeNode = None
        self.children: list[RelationalTreeNode] = []

    def add_child_body(self, child_body: CelestialBody) -> None:
        child = RelationalTreeNode(child_body)
        child.parent = self
        self.children.append(child)


class RelationalTree:
    def __init__(self, root_body: CelestialBody) -> None:
        self.root: RelationalTreeNode = RelationalTreeNode(root_body)

    def add_child_body(self, child_body: CelestialBody) -> None:
        self.root.add_child_body(child_body)

    @property
    def all_bodies(self) -> "list[RelationalTreeNode]":
        # Traverse the tree in a depth-first manner
        all_bodies: list[RelationalTreeNode] = []
        stack: list[RelationalTreeNode] = [self.root]
        while len(stack) > 0:
            node = stack.pop()
            all_bodies.append(node)
            stack.extend(node.children)
        return all_bodies

    @classmethod
    def solar_system(cls):
        tree = cls(CelestialBody.sun())
        tree.add_child_body(CelestialBody.mercury())
        tree.add_child_body(CelestialBody.venus())
        tree.add_child_body(CelestialBody.earth())
        tree.add_child_body(CelestialBody.mars())
        tree.add_child_body(CelestialBody.jupiter())
        tree.add_child_body(CelestialBody.saturn())
        tree.add_child_body(CelestialBody.uranus())
        tree.add_child_body(CelestialBody.neptune())
        return tree
