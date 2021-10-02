import numpy as np
import queue


class IVGraphNode:
    data = None
    x = None
    y = None

    def __init__(self, x, y, data):
        self.data = data
        self.x = x
        self.y = y

    def __str__(self):
        return "[" + str(self.data) + "]"


class IVGraph:
    nodes = None

    def __init__(self, width, height, val):
        graph = []#np.empty(shape=(width, height), dtype=np.object)
        #arr = val * np.ones((width, height))
        for row in range(height):
            row_arr = []
            for col in range(height):
                node = IVGraphNode(col, row, val)
                row_arr.append(node)
            graph.append(row_arr)

        self.nodes = graph

    def place_blocker(self,width,height,center_x,center_y,val):
        for row in range(len(self.nodes)):
            for col in range(len(self.nodes[row])):
                if row >= center_y - height/2 and row <= center_y + height/2:
                    if col >= center_x - width / 2 and col <= center_x + width / 2:
                        self.nodes[row][col].data = val

    def __str__(self):
        arr = ""
        for row in range(len(self.nodes)):
            row_str = ""
            for col in range(len(self.nodes[row])):
                row_str += (str(self.nodes[row][col])) + " "
            arr += row_str + "\n"

        return str(arr)


class IVAStarNode(IVGraphNode):
    start_node = None
    end_node = None
    Fx = " "  # total cost of this node
    Gx = " "  # actual dist of this node to start
    Hx = " "  # estimated distance of this node to end (manhattan distance)
    visited = False
    expanded = False
    is_solution_node = False
    parent = None  # node from which coming is how we get current Gx

    def __init__(self, x, y, data, start_node, end_node):
        super().__init__(x, y, data)
        self.start_node = start_node
        self.end_node = end_node

    def visit(self, visiting_node):
        old_gx = self.Gx
        self.Gx = visiting_node.Gx + self.data
        self.Hx = abs(self.x - self.end_node.x) + abs(self.y - self.end_node.y)
        self.Fx = self.Gx + self.Hx
        self.visited = True
        # if new visitor has a better path to this node than old path
        if old_gx == " " or old_gx > self.Gx:
            return True
        return False

    def __str__(self):
        if self.is_solution_node:
            return "[" + str(self.x) + " X " + str(self.y) + "]\n" + "[" + str(self.Fx) + " " + str(
                self.Gx) + " " + str(self.Hx) + "]"
        else:
            return "[" + str(self.x) + "   " + str(self.y) + "]\n" + "[" + str(self.Fx) + " " + str(
                self.Gx) + " " + str(self.Hx) + "]"


    def _is_valid_operand(self, other):
        return (hasattr(other, "Fx"))
    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.Fx == other.Fx
    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.Fx < other.Fx

def IVAStarPrint(start_node,end_node,starnodes,return_code,quiet = True):
    if not quiet:
        if return_code == 0:
            print("Solution")
        elif return_code == 1:
            print("No Traversible Path")
        else:
            print("Algorithm Error")
        graph_str = ""
        print("Key --- [Start: S] [End: E] [Solution Path: x] [Non-Traversible Start or End: !] [Non-Traversible: ^]\n--- --- [Non-0 Traversal Cost: [1-9]] [Non-0 Traversal Cost if part of solution path: *] ")
        for node_row in starnodes:  # np.nditer(graph.nodes, flags=['refs_ok']):
            row_str = ""
            for node in node_row:
                char = "."
                if start_node.x == node.x and start_node.y == node.y and node.data == 0:
                    char = "!"
                elif end_node.x == node.x and end_node.y == node.y and node.data == 0:
                    char = "!"
                elif start_node.x == node.x and start_node.y == node.y:
                    char = "S"
                elif end_node.x == node.x and end_node.y == node.y:
                    char = "E"
                elif node.data == 0:
                    char = "^"
                elif node.data != 1 and not node.is_solution_node:
                    char = str(node.data)
                elif node.data != 1 and node.is_solution_node:
                    char = "*"
                elif node.is_solution_node:
                    char = "x"

                row_str += char + " "
            graph_str += row_str + "\n"
        print(graph_str)

def IVAStar(start_node, end_node, graph, quiet = True):
    """ Determines best path between start_node and end_node along 2D grid of graph
    inputs:
    start_node: IVGraphNode containing x,y coordinates and data
    end_node: IVGraphNode containing x,y coordinates and data
    graph: 2D List of IVGraphNodes, relative position in the graph must match each nodes x,y coords
    eg, node at graph[0][0] must have node.x = 0 and node.y = 0
    quiet: whether to display debug output/visualization


    returns tuple, (return_code, [solution_path])
    where solution path is a list of the nodes from end to start
    where return code is:
    0 = solution found
    1 = solution not found, path was not found due to never reaching end (no traversible path exists)
    2 = solution not found, path was not found due to error (a bug in the algorithm implementation)
    """

    #print("Running A Star")


    starnodes = []
    return_code = 2
    solution_path = []
    open_nodes = queue.PriorityQueue()
    closed_nodes = queue.PriorityQueue()
    #print("Converting input...")
    for node_row in graph.nodes:#graph.nodes.__array__():  # np.nditer(graph.nodes, flags=['refs_ok']):
        starrow = []
        for node in node_row:
            starnode = IVAStarNode(node.y, node.x, node.data, start_node, end_node)
            starrow.append(starnode)
        starnodes.append(starrow)

    start_node = starnodes[start_node.x][start_node.x]

    if start_node.data == 0:
        IVAStarPrint(start_node,end_node,starnodes,1,quiet)
        return (1,solution_path)

    start_node.Fx = 0
    start_node.Gx = 0
    start_node.Hx = 0

    open_nodes.put((0, start_node))
    final_node = None

    #OPEN NODES - set of nodes to be evaluated. Marked as Expanded == False and are in the open_nodes queue
    #CLOSED NODES - nodes that have been evaluated

    #while there are still nodes to be evaluated
    while not open_nodes.empty():
        #print("Open nodes: " + str(open_nodes.qsize()))
        #get the open node with the lowest Fx cost. This node will visit all of its neighbors to advance the path
        visiting_node = open_nodes.get()[1]
        #print(" ***** Node that is Visiting:\n" + str(visiting_node))
        #if this node is the end node, done
        if visiting_node.x == end_node.x and visiting_node.y == end_node.y:
            final_node = visiting_node
            return_code = 0
            break
        #visit each neighbor of the visiting node
        for visit_x in [-1, 0, 1]:
            for visit_y in [-1, 0, 1]:
                if visit_x == 0 and visit_y == 0:
                    continue #don't visit yourself...
                node_to_visit_x = visiting_node.x + visit_x
                node_to_visit_y = visiting_node.y + visit_y
                #check neighbor is in bounds of grid
                if node_to_visit_x >= 0 and node_to_visit_x < len(starnodes) and node_to_visit_y >= 0 and node_to_visit_y < len(starnodes[visiting_node.x]):
                    node_to_visit = starnodes[visiting_node.x + visit_x][visiting_node.y + visit_y]
                    #print(" + visiting node: :\n" + str(node_to_visit))
                    #if the node is not traversible or in the closed list (expanded)
                    if node_to_visit.data == 0 or node_to_visit.expanded:
                        continue
                    # mark if path from visiting_node to node_to_visit is better path to
                    # node to visit than previously recorded
                    found_better_path = False
                    # if in OPEN list (has been visited but not has been the visitor)
                    if node_to_visit.expanded is False and node_to_visit.visited is True:
                        # visit again. see if this visit is a better path to node_to_visit
                        found_better_path = node_to_visit.visit(visiting_node)
                    # if in CLOSED list (has been the visitor / been expanded) (should not happen)
                    elif node_to_visit.expanded is True and node_to_visit.visited is True:
                        # visit again
                        found_better_path = node_to_visit.visit(visiting_node)
                        node_to_visit.expanded = False
                        open_nodes.put((node_to_visit.Fx, node_to_visit))
                    # if not in the open or closed list (has not been visited or been the visitor)
                    elif node_to_visit.expanded is False and node_to_visit.visited is False:
                        # visit for first time
                        found_better_path = node_to_visit.visit(visiting_node)
                        #print("Opened node: \n" + str(node_to_visit))
                        open_nodes.put((node_to_visit.Fx, node_to_visit))
                    #If a better path was found, update the parent, creating a path from visiting node to visited
                    if found_better_path:
                        node_to_visit.parent = visiting_node
                        #print("Found better path from \n" + str(visiting_node) + " to \n" + str(node_to_visit))
        #now that visiting node has explored all of its neighbors, it is expanded/closed
        closed_nodes.put((visiting_node.Fx, visiting_node))
        visiting_node.expanded = True

    if visiting_node.x != end_node.x and visiting_node.y != end_node.y:
        return_code = 1
        final_node = closed_nodes.get()[1]
        while final_node.parent is None:
            final_node = closed_nodes.get()[1]
    #print("Closed node: \n" + str(visiting_node))



    parent = final_node
    iter = 0
    size = len(starnodes) * len(starnodes[0])
    while parent is not None and iter < len(starnodes) * len(starnodes[0]):
        parent.is_solution_node = True
        solution_path.append((parent.x,parent.y))
        parent = parent.parent
        iter += 1
    if iter > size - 1:
       return_code = 2

    IVAStarPrint(start_node, end_node, starnodes, return_code, quiet)


    return (return_code,solution_path)
