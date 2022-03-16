class Node:
    def __init__(self, parent):
        self.parent = parent
        self.children = {}
        self.values = []

    def add_key_value(self, key, value):
        self.children[key] = value

    def add_child_node(self, child_node):
        self.children[child_node.identifier] = child_node

