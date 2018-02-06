

class Node:
    def __init__(self, prevNode=None, nextNode=None, surface='', feature='') -> None:
        self.surface = surface
        self.feature = feature
        self.prev = prevNode
        self.next = nextNode

class Tagger:
    def __init__(self) -> None:
        pass

    def parseToNode(self, parsed_text: str):
        node = Node()
        return_node = node
        for i in parsed_text.split('\n'):
            if i == 'EOS' or i=='':
                surface = i
                feature = ''
            else:
                surface, feature = i.split('\t')
            nextNode = Node(prevNode=node, surface=surface, feature=feature)
            node.next = nextNode
            node = nextNode
        return return_node