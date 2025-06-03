class Graph():
    def __init__(self) -> None:
        # directed graph
        self.graphDict = {}
        self.parentDict = {}

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

    def removeNode(self, node:str, noOrphans:bool=False):
        # remove node and all links to it
        if node in self.graphDict:
            del self.graphDict[node]
            if noOrphans:
                for key in self.graphDict.keys():
                    if node in self.graphDict[key]:
                        self.graphDict[key].remove(node)

    def generateParentDict(self):
        # generate a dictionary of parents for each node
        for node, links in self.graphDict.items():
            for link in links:
                if link not in self.parentDict:
                    self.parentDict[link] = set()
                self.parentDict[link].add(node)

    def getParents(self, node):
        # find all parents of a node
        parents = set()
        for key, links in self.graphDict.items():
            if node in links:
                parents.add(key)
        return parents

    def getChildren(self, node):
        visited = []  # Use a list to maintain order of traversal
        queue = [node]  # Use a queue to process nodes breadth-first

        while queue:
            current = queue.pop(0)  # Get the next node in the queue
            if current not in visited:
                visited.append(current)  # Add to visited list
                for link in self.graphDict.get(current, set()):
                    if link not in visited and link not in queue:
                        queue.append(link)  # Add unvisited children to the queue
        return visited