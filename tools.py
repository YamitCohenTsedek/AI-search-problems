import heapq
from ways import info, load_map_from_csv
from ways.tools import compute_distance


# Node class represents a node of a graph for our routing problem.
class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0, cost_func=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.cost_function = cost_func
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    # Set the cost function of Node class.
    def set_cost_function(self, cost_func):
        self.cost_function = cost_func

    # Return all the children of the current node (in our problem: the junctions that the current junction linked to).
    def expand(self, problem):
        return [self.child_node(problem, link) for link in self.state.links]

    # Return a specific child of the current node by applying the given action on the node.
    def child_node(self, problem, action):
        next_state = problem.successor(self.state, action)
        next_node = Node(next_state, self, action, self.path_cost + self.cost_function(action), self.cost_function)
        return next_node

    # Create the solution path.
    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node.state.index)
            node = node.parent
        return list(reversed(path_back))

    # Return the solution of the problem - the path and the cost.
    def solution(self):
        return self.path(), self.path_cost
    
	# If the current state costs less than the other state - return True, otherwise - return False.
    def __lt__(self, other_node):
        return self.state < other_node.state

    # Compare the current node to the other node and return True if they are equal, otherwise - return False.
    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    # Return True if the current node is not the other node, otherwise return False.
    def __ne__(self, other):
        return not (self == other)

    # Return the hash value of the state of the current node.
    def __hash__(self):
        return hash(self.state)


# An implementation of a priority queue, based on a priority heap, which allows custom sorting function.
class PriorityQueue:
    def __init__(self, f=lambda x: x):
        self.heap = []
        self.f = f

    # Insert the specified item into the priority queue.
    def append(self, item):
        heapq.heappush(self.heap, (self.f(item), item))

    # Insert the specified items into the priority queue.
    def extend(self, items):
        for item in items:
            self.append(item)

    # Retrieve and remove the head of the priority queue, or throw an exception if the queue is empty.
    def pop(self):
        if self.heap:
            return heapq.heappop(self.heap)[1]
        else:
            raise Exception('The priority queue is empty.')

    # Return the length of the priority queue.
    def __len__(self):
        return len(self.heap)

    # Return True if the desired key is in the priority queue, otherwise - return False.
    def __contains__(self, key):
        return any([item == key for _, item in self.heap])

    # Get the value of the given key if it is in the priority queue, otherwise - return None.
    def __getitem__(self, key):
        for value, item in self.heap:
            if item == key:
                return value
        return None

    # If the specified key is in the priority queue delete it, otherwise - throw an exception.
    def __delitem__(self, key):
        try:
            del self.heap[[item == key for _, item in self.heap].index(True)]
        except ValueError:
            raise KeyError(str(key) + " is not in the priority queue")
        heapq.heapify(self.heap)


# RoutingProblem class represents a problem in which we want to find the cheapest route
# from its start state to its goal state.
class RoutingProblem:
    def __init__(self, start_state, goal, g):
        self.g = g
        self.start_state = self.g.get(start_state)
        self.goal = self.g.get(goal)

    # Return the state that results from applying action a on state s,
    # or throw an exception if there's no route from s to a.
    def successor(self, s, a):
        state = self.g.get(a.target)
        if state is None:
            raise ValueError(f'No route from {s} to {a}')
        return state

    # Return True if the given state is the goal state, otherwise - return False.
    def is_goal(self, s):
        return s == self.goal


# MapData class is a singleton of the roads map data.
class MapData:
    __instance = None
    @staticmethod
    def get_instance():
        # Static access method.
        if MapData.__instance is None:
            MapData()
        return MapData.__instance

    def __init__(self):
        # Virtually private constructor.
        if MapData.__instance is None:
            MapData.__instance = load_map_from_csv()


# The cost function of our routing problem is the traveling time from junction to junction.
def cost_function(action):
    # Get the velocity of the link according to the highway type of it.
    velocity = info.SPEED_RANGES[action.highway_type][1]
    # Equation of motion: velocity * time = distance
    # => time = distance / velocity
    time_cost = action.distance / 1000 / velocity
    # Covert the time to seconds and return the result.
    return time_cost


# The heuristic function is the air distance between the two junctions / the maximal possible road speed.
def heuristic_function(first_node, second_node):
    max_speed = 110
    return compute_distance(first_node.state.lat, first_node.state.lon, second_node.state.lat,
                            second_node.state.lon) / max_speed
