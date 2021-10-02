# IVAStar
An implementation of AStar Pathfinding in Python

    Determines best path between start_node and end_node along 2D grid of graph
    inputs:
    start_node: arbitray class node containing x,y coordinates and data
    end_node: arbitray class node containing x,y coordinates and data
    graph: 2D List of arbitray class nodes, relative position in the graph must match each nodes x,y coords
    eg, node at graph[0][0] must have node.x = 0 and node.y = 0
    quiet: whether to display debug output/visualization
    
    All nodes must have x,y coordinate and data. Data is the traversal cost of the node
    0 - not traversible
    1 - free traversal
    2-9 - non-zero traversal cost where 2 is double the cost of 1


    returns tuple, (return_code, [solution_path])
    where solution path is a list of the nodes from end to start
    where return code is:
    0 = solution found
    1 = solution not found, path was not found due to never reaching end (no traversible path exists)
    2 = solution not found, path was not found due to error (a bug in the algorithm implementation)
 
    
    Included demo sample output:
    
    
![image](https://user-images.githubusercontent.com/60797163/135728006-e1f84d4e-4e53-4a94-a4ca-5261f22a0446.png)

Basic path:

![image](https://user-images.githubusercontent.com/60797163/135728015-47b70a14-aef5-46b9-804a-ca3d154b0387.png)

Path avoiding non-traversible nodes ('^')

![image](https://user-images.githubusercontent.com/60797163/135728038-aca98b80-a3e4-4a9c-8c90-d6568e20b9c6.png)

Path avoiding non-traversible nodes and taking expensive node paths when it is the best option ('*'indicates non-free node in solution path)

![image](https://user-images.githubusercontent.com/60797163/135728123-00da35e8-5f75-44ce-8ed2-6ac8862887dc.png)

Path where there is no solution

![image](https://user-images.githubusercontent.com/60797163/135728150-a5112d33-aa01-41be-8e0d-2fff9a9f158a.png)






    
