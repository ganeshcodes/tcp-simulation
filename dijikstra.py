def dijkstra(graph,src,dest,visited=[],distances={},predecessors={}):

    """ calculates a shortest path tree routed in src

    """   
    print("calculating shortest path")
    # a few sanity checks

    if src not in graph:

        raise TypeError('The root of the shortest path tree cannot be found')

    if dest not in graph:

        raise TypeError('The target of the shortest path cannot be found')   

    # ending condition

    if src == dest:

        # We build the shortest path and display it

        path=[]

        pred=dest

        while pred != None:

            path.append(pred)

            pred=predecessors.get(pred,None)

        print('shortest path: '+str(path)+" cost="+str(distances[dest]))

    else :    

        # if it is the initial  run, initializes the cost

        if not visited:

            distances[src]=0

        # visit the neighbors

        for neighbor in graph[src] :

            if neighbor not in visited:

                new_distance = distances[src] + graph[src][neighbor]

                #print({}.format(distances.get(neighbor,float('inf')))
                print("dfds")
                              
                if new_distance < distances.get(neighbor,float('inf')):

                    distances[neighbor] = new_distance

                    predecessors[neighbor] = src

        # mark as visited

        visited.append(src)

        # now that all neighbors have been visited: recurse                        

        # select the non visited node with lowest distance 'x'

        # run Dijskstra with src='x'

        unvisited={}

        for k in graph:

            if k not in visited:

                unvisited[k] = distances.get(k,float('inf'))       

        x=min(unvisited, key=unvisited.get)

        dijkstra(graph,x,dest,visited,distances,predecessors)

 

if __name__ == "__main__":

    #import sys;sys.argv = ['', 'Test.testName']

    #unittest.main()
    import sys
    
    sourcePort = int(sys.argv[1])
    destPort = int(sys.argv[2])
    
    print(sourcePort)
    print(destPort)

    graph = {'a': {'b': 4, 'c': 3, 'e':7},

            'b': {'a': 4, 'c': 6, 'l':5},

            'c': {'a': 3, 'b': 6, 'd': 11},

            'd': {'c': 11, 'f': 6, 'g': 10, 'l':9},

            'e': {'a': 7, 'g': 5},

            'f': {'d': 6, 'l': 5},

            'g': {'d':10, 'e':5},

            'l': {'b':5, 'd':9, 'f':5}}

             

    #Ann-Chan

    if(sourcePort == 2001 and destPort == 2003):

        dijkstra(graph,'a','e')
             

    #Ann-Jan

    if(sourcePort == 2001 and destPort == 2002):

        dijkstra(graph,'a','f')



    #Chan-Ann

    if(sourcePort == 2003 and destPort == 2001):

        dijkstra(graph,'e','a')



    #Chan-Jan

    if(sourcePort == 2003 and destPort == 2002):

        dijkstra(graph,'e','f')



    #Jan-Ann

    if(sourcePort == 2002 and destPort == 2001):

        dijkstra(graph,'f','a')



    #Jan-Chan

    if(sourcePort == 2002 and destPort == 2003):

        dijkstra(graph,'f','e')