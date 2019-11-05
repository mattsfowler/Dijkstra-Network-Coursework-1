infinity = 1000000
invalid_node = -1

class Node:
    previous = invalid_node
    distfromsource = infinity
    visited = False

class Dijkstra:

    def __init__(self):
        '''initialise class'''
        self.startnode = 0
        self.endnode = 0
        self.network = []
        self.network_populated = False
        self.nodetable = []
        self.nodetable_populated = False
        self.route = []
        self.route_populated = False
        self.currentnode = 0


    # ----- PUBLIC METHODS (fixed interface) ----- 

    def populate_network(self, filename):
        '''populate network data structure'''
        # Set all flags to false, to indicate no calculations have been done on this network
        self.network = []
        self.network_populated = False
        self.nodetable_populated = False
        self.route_populated = False

        # Read from the given file and normalise the input
        # Try to open the file and read it's contents
        f = None
        try:
            f = open(filename, "r")
        except FileNotFoundError:
            print("ERROR: file does not exist")
            return

        # The int conversion could have been done in the same line as the appending and splitting.
        # I feel that separating the lines is more readable, even if it sacrifices efficiency.
        for line in f.readlines():
            self.network.append(line.split(","))
            try:
                # Values are strings -> convert to integers
                self.network[-1] = [int(col) for col in self.network[-1]]
            except ValueError:
                print("ERROR: non-number found in the matrix")
                f.close()
                return
        f.close() # We've read everything now, no need to keep it open

        # Validate the given file
        height = len(self.network)
        for row in self.network:
            if len(row) != height:
                print("ERROR: matrix width does not match matrix height")
                return

        # Indicate to any methods that need access to the network that the network has been
        #  successfully loaded.
        self.network_populated = True

    def populate_node_table(self):
        '''populate node table'''
        # Can't be performed before the network is loaded
        if not self.network_populated:
            print("ERROR: no network loaded")
            return

        # Create a default node for each node detected in the network
        # Except the starting node, whose distance is set to 0 and is immediately marked as visited
        self.nodetable = [Node() for i in range(len(self.network))]
        self.nodetable[self.startnode].visited = True
        self.nodetable[self.startnode].distfromsource = 0
        self.currentnode = self.startnode
        self.nodetable_populated = True

    def parse_route(self, filename):
        '''load in route file'''
        # Read from the given file and normalise the input
        # Try to open the file and read it's contents
        f = None
        try:
            f = open(filename, "r")
        except FileNotFoundError:
            print("ERROR: file does not exist")
            return []

        line = f.read()
        f.close()
        # Remove whitespaces and separate start/end nodes
        line = "".join(line.split("\n"))
        line = "".join(line.split(" "))
        line = line.split(">")

        if len(line) != 2:
            print("ERROR: file must contain exactly 1 '>' seperator")
        else:
            self.startnode = ord(line[0]) - 65
            self.endnode = ord(line[1]) - 65
            
        
    def return_near_neighbour(self):
        '''determine nearest neighbours of current node'''
        # Can't be performed without a network loaded, but can be done without the nodetable loaded.
        if not self.network_populated:
            print("ERROR: no network loaded")
            return []

        # Iterates through each node in the network, and checks the cost to travel to currentnode.
        # Don't add a node only if the cost is 0, indicating no connection.
        neighbours = []
        for node in range(len(self.network[self.currentnode])):
            if not self.network[self.currentnode][node] == 0:
                neighbours.append(node)
        return neighbours
            

    def calculate_tentative(self):
        '''calculate tentative distances of nearest neighbours'''
        if not self.network_populated or not self.nodetable_populated:
            print("ERROR: no network loaded, or no nodetable not initialised")
            return
        
        neighbours = self.return_near_neighbour()
        for n in neighbours:
            # If this neighbour is unvisited, check how far from the source it would be if the
            #  path traveled through currentnode.
            if not self.nodetable[n].visited:
                tentative = self.nodetable[self.currentnode].distfromsource + self.network[self.currentnode][n]
                if tentative < self.nodetable[n].distfromsource:
                    self.nodetable[n].distfromsource = tentative
                    self.nodetable[n].previous = self.currentnode

    def determine_next_node(self):
        '''determine next node to examine'''
        if not self.network_populated or not self.nodetable_populated:
            print("ERROR: no network loaded, or no nodetable not initialised")
            return

        nextnode = invalid_node
        lowestdist = infinity

        # Searches the nodetable for the closest node to the source that is invisited.
        # Does not alter any object attributes, only returns the node as an int.
        # If all nodes have been visited, will return value of 'invalid_node'.
        for n in range(len(self.nodetable)):
            if not self.nodetable[n].visited:
                if self.nodetable[n].distfromsource < lowestdist:
                    lowestdist = self.nodetable[n].distfromsource
                    nextnode = n
        return nextnode
      
    def calculate_shortest_path(self):
        '''calculate shortest path across network'''
        if not self.network_populated:
            print("ERROR: no network loaded")
            return
        
        self.route = []
        self.populate_node_table()
        self.route_populated = False

        # Once tentative distances have been calculated, find closest unvisited node to source.
        # Mark this node as visited, and set it to be the new current node.
        # Repeat until either the target (endnode) is the currentnode, or until all of the
        #  nodes have been visited.
        while not (self.currentnode == self.endnode): 
            self.calculate_tentative()
            self.currentnode = self.determine_next_node()
            self.nodetable[self.currentnode].visited = True
            if self.currentnode == invalid_node:
                break

        # If the currentnode is not the target node, the algorithm could not find a solution.
        # If a path was found, walk backwards through nodetable using the 'previous' attribute
        #  as the pointer to the next node.
        # Place each node that was walked through at the begining of the route attribute.
        if self.currentnode == self.endnode:
            while self.currentnode != self.startnode:
                self.route = [self.currentnode] + self.route
                self.currentnode = self.nodetable[self.currentnode].previous
            self.route = [self.startnode] + self.route
            self.route_populated = True
        

    def return_shortest_path(self):
        '''return shortest path as list (start->end), and total distance'''
        if not self.route_populated:
            print("ERROR: no path calculated / loaded")
            return []
        else:
            return self.route


class MaxFlow(Dijkstra): 
    '''inherits from Dijkstra class. 
    Expose and override Dijkstra methods and add new ones where required, but must use original Dijkstra’s algorithm as part of the calculation'''

    def __init__(self):
        Dijkstra.__init__(self)
        self.bottleneck = 0
        self.bottleneck_populated = False
        self.totalflow = 0
        self.totalflow_populated = False

    def find_bottleneck(self):
        '''finds the value of the lowest cost edge in self.route'''
        if not self.route_populated:
            print("ERROR: no route to search")
            return

        print("Found route: " + ">".join([str(chr(n + 65)) for n in self.route]), end="")

        # Simply returns the lowest cost edge in the route (calculated using Dijkstra's algorithm),
        #  and prints the information to the console. Loops through each pair of neighbouring
        #  nodes in the route, finding the distance between them each time. The lowest distance
        #  is the bottleneck flow.
        self.bottleneck = infinity
        for i in range(len(self.route) - 1):
            edge_cost = self.network[ self.route[i] ][ self.route[i + 1] ]
            if edge_cost < self.bottleneck:
                self.bottleneck = edge_cost
        print(", with a bottleneck flow of " + str(self.bottleneck))
        self.bottleneck_populated = True


    def reduce_weights(self):
        '''reduces the value of each edge in the current route by the bottleneck value'''
        if not self.bottleneck_populated:
            print("ERROR: no bottleneck value calculated")
            return

        # Travels through the route, subtracting the bottleneck value in the direction of flow,
        #  and adding it to the opposite direction to allow for imaginary reverse flow.
        for i in range(len(self.route) - 1):
            self.network[ self.route[i] ][ self.route[i + 1] ] -= self.bottleneck
            self.network[ self.route[i + 1] ][ self.route[i] ] += self.bottleneck
        self.totalflow += self.bottleneck
        self.bottleneck_populated = False
        

    def calculate_max_flow(self):
        '''prints out each path used along with it's bottleneck value, and the total flow through the network'''
        # 1. calculate shortest path using Dijkstra's algorithm
        # 2. work out the smallest weight along this path
        # 3. subtract this value from each edge in the path
        # 3.5. add this value in the opposite direction (imaginary reverse flow, Ford Fulkerson)
        # 4. add this value to the totalflow
        # 5. repeat until no valid path can be found using Dijkstra
        if not self.network_populated:
            print("ERROR: no network loaded")
            return

        # Setup - make sure an initial route is calculated before continuing
        self.bottleneck_populated = False
        self.totalflow_populated = False
        self.calculate_shortest_path()
        if not self.route_populated:
            print("ERROR: no route to the sink can be found, flow is 0")

        # Algorithm will reduce cost of each edge in the route found in each itereration.
        # Will complete when no valid route can be found using "calculate_shortest_path"
        while self.route_populated:
            self.find_bottleneck()
            self.reduce_weights()
            self.calculate_shortest_path()
        self.totalflow_populated = True
        self.network_populated = False #network values have been altered, network is no longer valid

    def return_max_flow(self):
        '''returns the max flow from the source (startnode) to the sink (endnode)'''
        if not self.totalflow_populated:
            print("ERROR: no flow calculated")
            return 0
        else:
            return self.totalflow

