from Dijkstra import Dijkstra, MaxFlow


if __name__ == "__main__":

    print(" ----- EXAMPLE NETWORK -----")
    ExampleNetwork = MaxFlow()
    ExampleNetwork.populate_network("network.txt")
    ExampleNetwork.parse_route("route.txt")
    ExampleNetwork.calculate_shortest_path()

    for row in ExampleNetwork.network:
        for col in row:
            print(str(col) + "|",end="")
        print()
    print("Finding shortest path between ", end="")
    print(chr(ExampleNetwork.startnode + 65) + " and ", end="")
    print(chr(ExampleNetwork.endnode + 65))
    print("Route Found: " + " > ".join([chr(x + 65) for x in ExampleNetwork.return_shortest_path()]))

    print("Finding max flow...")
    ExampleNetwork.calculate_max_flow()
    print("Total flow = " + str(ExampleNetwork.return_max_flow()))
    print()


    print(" ----- TEST REVERSE FLOW NETWORK -----")
    RevFlowTest = MaxFlow()
    RevFlowTest.populate_network("network2.txt")
    RevFlowTest.parse_route("route2.txt")
    RevFlowTest.calculate_shortest_path()

    for row in RevFlowTest.network:
        for col in row:
            print(str(col) + "|",end="")
        print()
    print("Finding shortest path between ", end="")
    print(chr(RevFlowTest.startnode + 65) + " and ", end="")
    print(chr(RevFlowTest.endnode + 65))
    print("Route Found: " + " > ".join([chr(x + 65) for x in RevFlowTest.return_shortest_path()]))

    print("Finding max flow...")
    RevFlowTest.calculate_max_flow()
    print("Total flow = " + str(RevFlowTest.return_max_flow()))


    print()
    print(" ----- NETWORK FROM SLIDES -----")
    SlidesNetwork = MaxFlow()
    SlidesNetwork.populate_network("network3.txt")
    SlidesNetwork.parse_route("route3.txt")
    SlidesNetwork.calculate_shortest_path()

    for row in SlidesNetwork.network:
        for col in row:
            print(str(col) + "|",end="")
        print()
    print("Finding shortest path between ", end="")
    print(chr(SlidesNetwork.startnode + 65) + " and ", end="")
    print(chr(SlidesNetwork.endnode + 65))
    print("Route Found: " + " > ".join([chr(x + 65) for x in SlidesNetwork.return_shortest_path()]))

    print("Finding max flow...")
    SlidesNetwork.calculate_max_flow()
    print("Total flow = " + str(SlidesNetwork.return_max_flow()))
