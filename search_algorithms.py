import sys
from tools import Node, PriorityQueue, RoutingProblem, MapData, cost_function, heuristic_function


# Best first graph search algorithm explores a graph by expanding the most promising
# node chosen according to a cost function - f, and also deals with loops.
def best_first_graph_search(problem, cost_func, f):
    # Create the node of the initial state and set its cost function.
    node = Node(problem.start_state)
    node.set_cost_function(cost_func)
    frontier = PriorityQueue(f)  # The frontier is implemented as a Priority Queue.
    frontier.append(node)
    closed_list = set()  # Set a closed list to deal with loops.
    while frontier:  # As long as the frontier is not empty
        node = frontier.pop()  # Retrieve and remove the head of the priority queue.
        # If the state of the current node is the goal state - return the solution (the path and cost).
        if problem.is_goal(node.state):
            return node.solution()
        closed_list.add(node.state.index)  # Add the current state to the closed list
        for child in node.expand(problem):  # Run over the children of the current node.
            child_item = frontier.__getitem__(child)
            # If the child is not in the frontier and also not in the closed list - insert it to the frontier.
            if child.state.index not in closed_list and child_item is None:
                frontier.append(child)
            # If the child is in the frontier and we have found a shorter path to it -
            # delete the longer path from the frontier and save the shorter path instead.
            elif child_item is not None and f(child) < child_item:
                del frontier[child]
                frontier.append(child)
    return None


# Return the path cost of a specified node.
def g(node):
    return node.path_cost


# Solve a routing problem according to UCS algorithm.
def find_ucs_route(source, target):
    problem = RoutingProblem(source, target, MapData.get_instance())
    # Use best first graph search algorithm when function f defined as g (the path cost), and return the solution path.
    return best_first_graph_search(problem, cost_function, f=g)[0]


# Greedy best first graph search algorithm uses best first graph search to refer specifically to a search
# with a heuristic that attempts to predict how close the end of a path is to a solution
# so that paths which are judged to be closer to a solution are extended first.
def greedy_best_first_graph_search(problem, h):
    return best_first_graph_search(problem, f=h)


# Solve a routing problem according to A* algorithm.
def find_astar_route(source, target):
    problem = RoutingProblem(source, target, MapData.get_instance())
    # Use best first graph search algorithm when function f defined as g (the path cost) + h (the heuristic function)
    # and return the solution path.
    return best_first_graph_search(problem, cost_function,
                                   f=lambda n: g(n) + heuristic_function(n, Node(problem.goal)))[0]


# Implementation of "DFScountour" - it gets the current limit and returns a new limit.
def depth_limited_search(path, cost, limit, problem, cost_func, f):
    last_node = path[-1]  # Save the last node of the path in last_node.
    last_node.set_cost_function(cost_func)
    cost = f(last_node)  # Find the cost of the last node.
    # If the cost of the node is greater then the limit, return the cost.
    if cost > limit:
        return cost
    # If the current node state is a goal state, return "Found" which indicates that a route was found.
    if problem.is_goal(last_node.state):
        return "Found"
    minimum = sys.maxsize
    for succ in last_node.expand(problem):  # Run over the children of the current node
        path.append(succ)
        # Recursive call to depth_limited_search.
        t = depth_limited_search(path, cost + g(last_node), limit, problem, cost_func, f)
        # If a route was found, return "Found".
        if t == "Found":
            return "Found"
        # If t is smaller then the minimum, update the minimum to be t.
        if t < minimum:
            minimum = t
        path.pop()  # Pop the last node from the path.
    return minimum  # Return the minimum.


# IDA* finds the shortest path from a start state to a goal state in a weighted graph.
# It uses a heuristic function to evaluate the remaining cost to get to the goal from the A* search algorithm.
# it concentrates on exploring the most promising nodes and thus does not go to the same depth everywhere.
def idastar(problem):
    # The initial limit is the evaluation of the heuristic function from the start state to the goal state.
    limit = heuristic_function(Node(problem.start_state), Node(problem.goal))
    path = [Node(problem.start_state)]  # Set the start state as the first node of the path.
    cost = 0
    while limit < sys.maxsize:
        # An implementation of "DFScountour" - it gets the current limit and returns a new limit.
        t = depth_limited_search(path, cost, limit, problem,
                                 cost_function, f=lambda n: g(n) + heuristic_function(n, Node(problem.goal)))
        if t == "Found":
            path_indexes = []  # Create the list of the path indexes and return it.
            for junction in path:
                path_indexes.append(junction.state.index)
            return path_indexes
        if t == sys.maxsize:
            return "Not Found"
        limit = t  # Set the old limit to be the new limit.


# Solve a routing problem according to IDA* algorithm.
def find_idastar_route(source, target):
    problem = RoutingProblem(source, target, MapData.get_instance())
    return idastar(problem)


