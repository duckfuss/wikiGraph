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
    
    def getChildren(self, node):
        visited = []  # Use a list to maintain order of traversal
        queue = [node]  # Use a queue to process nodes breadth-first

        while queue:
            current = queue.pop(0)  # Get the next node in the queue
            if current not in visited:
                print(f"Visiting node: {current}")  # Debug print
                visited.append(current)  # Add to visited list
                for link in self.graphDict.get(current, set()):
                    print(f"  {current} -> {link}")  # Debug print
                    if link not in visited and link not in queue:
                        queue.append(link)  # Add unvisited children to the queue
        return visited