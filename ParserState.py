from Node import Node


class ParserState:
    def __init__(self):
        self.current_node = Node(None)
        self.current_identifier = None
        self.within_quotes = False

