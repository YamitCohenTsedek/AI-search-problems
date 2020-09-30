# AI-search-problems

### Description of Israel.csv file structure (location: db/Israel.zip/Israel.csv):
Each row represents a junction on the map and contains information about it. <br />
Each row is divided into several columns as follows:<br />
Column 1: index - the index of the node, an int type field.<br />
Column 2: lat - latitude, the latitude of the node - a float type field.<br />
Column 3: lon - longitude - the longitude of the node - a float type field.<br />
The following columns: list of links to nodes to which there is a route from the current node.<br />

The structure of the links is as follows: target@distance@highway_type, where target (an int type field) represents the index of the destination node, distance (a float type field) represents the distance from it, and highway_type (an int type field) represents the type of the road that leading to it.


### Description of problems.csv file structure:
The file contains 100 random search problems. Each row in the file represents a search problem, with the left index representing a start node and the right index representing a target node.<br />
In the solutions file of UCS algorithm (location: results/UCSRuns.txt) each row contains the cost of the route of the corresponding problem.<br />
In the solutions files of A* and IDA* algorithms (locations: results/AStarRuns.txt, results/IDAStarRuns.txt), each row contains the heuristic evaluation on the left and the cost of the route on the right.


### Description of the cost function structure (location: tools.py):
Signature: cost_function(link).<br />
Input: a Link object. The cost function calculates the cost of the travel time from a certain node to a node that is linked to it, thus the function gets as a parameter the link between the two nodes, to extract information such as the distance between the two nodes, and the maximum speed allowed on the connecting road.<br />
Output: the travel time from a certain node to a node linked to it, in time units of hours.<br />
Calculated by the equation of motion: velocity * time = distance => time = distance / velocity.                                              


### Description of the heuristic function structure (location: tools.py):
Signature: heuristic_function(first_junction, second_junction).<br />
Input: Two Junction objects.<br />
Output: the estimated travel time between the two junctions. The output of the heuristic function is the calculation of the estimated distance (the air distance) between the junctions, divided by the maximum possible travel speed (110 km / h).<br />
This heuristic function is admissible, i.e. - underestimate.<br />
First, it is easy to see that it is non-negative, and h(goal)=0, since the distance from the goal to itself is 0.<br />
Now, if we mark the cheapest route from an arbitrary junction to the target junction as h* and our heuristic function as h, then the estimate of h will always be ≤ than the value of h*, i.e. - it is optimistic. That is because there can be no route from the start junction to the target junction whose traveling time is faster than the traveling time of the aerial distance between the junctions (which is the minimum distance between them), with the maximum possible traveling velocity.


### A graph representing the runs of A* algorithm on the 100 search problems:
![AStarCosts](https://user-images.githubusercontent.com/45918740/94563147-f1200e00-026e-11eb-9fb3-b1b6efa7bda2.png)

The above graph shows us the relationship between the actual travel times (X) and the travel times estimated by the heuristic function (Y).<br />
It can be seen that all the points (x, y) are not below the line y=x, i.e. - for each point, its y-value is necessarily ≥ than its x-value.<br />
That means that the travel times estimated by the heuristic are always ≤ than the actual travel times. Therefore, this heuristic is acceptable, since it is optimistic - it always gives an estimation that is smaller or equal to the real cost, and never higher than the actual cost.

### The average runtimes of the algorithms (excluding map loading time):
For UCS algorithm: the total runtime of 100 problems was 10.818 seconds, so the average runtime is: 0.108 seconds.<br />
For A* algorithm: the total runtime of 100 problems was 3.522 seconds, so the average runtime is: 0.035 seconds.<br />
For IDA* algorithm: the total runtime of 5 problems was 4.664 seconds, so the average run time is: 0.933 seconds.<br />
As we can see, the algorithm that runs in the shortest time is A*.<br />

The reason why A* is faster than UCS: the UCS algorithm is an Uninformed search algorithm, which means that it does not use information from the world to speed up the search. A* is an Informed search algorithm, it does use information from the world, embodied in the heuristic function, to guess which nodes are more "promise" and develop them first. Therefore, when the heuristics are good enough, Informed search algorithms usually have a better running time, and in our case, as explained - the function is acceptable. The estimations of the heuristic function do help to improve the running times.<br />

The reason why A* is faster than IDA*: note that A* is implemented as a graph search and IDA* is implemented as a tree search. That is, A* avoids repetitive developments when they do not improve the cost. On the other hand, the implementation of IDA* may develop nodes again and again, without knowing they were already visited.
Therefore, the runtime of A* algorithm may be shorter than the runtime of IDA* algorithm (as can be seen in the average running times shown above).
