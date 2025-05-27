class Graph():
    def __init__(self) -> None:
        # directed graph
        self.graphDict = {}

    def addNode(self, node:str, links:set):
        # add links to node if node is new
        if node not in self.graphDict.keys():
            self.graphDict[node] = links
        # updates a seen node's links
        else:
            self.graphDict[node].update(links)
        # add any implicit linked nodes that aren't in graph dict
        for link in links:
            if link not in self.graphDict.keys():
                self.graphDict[link] = set()
    
    def getChildren(self, node, childSet=None):
        if childSet is None:
            childSet = set()  # Initialize childSet if not provided
        if node in childSet:
            return childSet  # Avoid revisiting nodes
        childSet.add(node)  # Add the current node to the childSet
        for link in self.graphDict.get(node, set()):  # Traverse outgoing links
            self.getChildren(link, childSet)  # Recursively get children
        return childSet