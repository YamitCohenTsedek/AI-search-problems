import matplotlib.pyplot as p
from tools import Node, RoutingProblem, MapData, cost_function, heuristic_function
from search_algorithms import best_first_graph_search, idastar, g
from ways import tools


# 100 arbitrary solvable search problems.
def get_100_solvable_search_problems():
    return [(800171, 800163), (800670, 476654), (174, 754562), (1, 906032), (882261, 864601), (533819, 816869),
            (95288, 95299), (195249, 338511), (511870, 511876), (374279, 374281), (486236, 490721), (332255, 332267),
            (108564, 107169), (239250, 280361), (60656, 10707), (390667, 390681), (293760, 322856), (938426, 938450),
            (783877, 592196), (915775, 915735), (667596, 667575), (889728, 10900), (651269, 651286), (162055, 162083),
            (658402, 658437), (102922, 102931), (401260, 391279), (808205, 808215), (38000, 38953), (206971, 199325),
            (224239, 282965), (20, 530299), (45, 7039), (118, 87711), (160, 539732), (177, 538356), (214, 535968),
            (549, 880713), (550727, 802140), (283438, 745963), (278000, 268096), (185586, 170840), (76, 698674),
            (698526, 611721), (65078, 65116), (12054, 561042), (759211, 759088), (856730, 423), (98821, 730873),
            (593549, 870265), (493222, 492200), (500661, 498180), (660988, 660997), (1075, 890), (647497, 647502),
            (513438, 513419), (581328, 593237), (551942, 552020), (901413, 475261), (250535, 283500), (26, 527802),
            (381, 95852), (398, 856724), (838794, 838821), (17, 23184), (5052, 3743), (8, 37396), (37430, 37061),
            (161031, 161075), (161086, 161122), (171, 879203), (100000, 99119), (623832, 623799), (734347, 685478),
            (312544, 266397), (629529, 70171), (750431, 840752), (750983, 605941), (759378, 703306), (763540, 666390),
            (847540, 922499), (40, 871810), (100, 544441), (3000, 12776), (10000, 899782), (902513, 527280),
            (906991, 928808), (907972, 40829), (228, 464784), (925275, 925145), (100747, 93312), (314893, 279733),
            (167, 884971),(5000, 764257), (20202, 20242), (10109, 31378), (32016, 724336), (648650, 553166),
            (944766, 29534), (678930, 678939)]


# Write the 100 problems in a csv file.
def write_problems_in_csv():
    import csv
    arbitrary_solvable_problems = get_100_solvable_search_problems()
    with open('problems.csv', mode='w', newline='') as problems_file:
        problems_writer = csv.writer(problems_file, delimiter=',')
        for problem in arbitrary_solvable_problems:
            problems_writer.writerow([str(problem[0]), str(problem[1])])


# Load the 100 problems from problems.csv and return them as a list.
def load_data():
    problems_list = []
    import csv
    with open('problems.csv', mode='r') as problems_file:
        problems_reader = csv.reader(problems_file)
        for line in problems_reader:
            problems_list.append((line[0], line[1]))
    return problems_list


# Write the costs of the 100 problems according to UCS algorithm in results/UCSRuns.txt.
def ucs_solution_for_100_problems():
    ucs_results_file = open('results/UCSRuns.txt', "w")
    problems_list = load_data()
    for problem in problems_list:
        source = problem[0]
        target = problem[1]
        problem = RoutingProblem(int(source), int(target), MapData.get_instance())
        ucs_results_file.write(str(best_first_graph_search(problem, cost_function, f=g)[1]) + "\n")
    ucs_results_file.close()

# Compute the runtime of UCS algorithm for 100 problems.
@tools.timed
def ucs_runtime():
    arbitrary_solvable_problems = get_100_solvable_search_problems()
    for problem in arbitrary_solvable_problems:
        source = problem[0]
        target = problem[1]
        problem = RoutingProblem(source, target, MapData.get_instance())
        best_first_graph_search(problem, cost_function, f=g)


# Write in results/AStarRuns.txt the costs and the heuristic evaluations 
# (from a start state to a goal state) of the 100 problems according to AStar algorithm.
def astar_solution_for_100_problems():
    astar_results_file = open('results/AStarRuns.txt', "w")
    problems_list = load_data()
    counter = 0
    for problem in problems_list:
        source = problem[0]
        target = problem[1]
        problem = RoutingProblem(int(source), int(target), MapData.get_instance())
        path, cost = best_first_graph_search(problem, cost_function, f=lambda n: g(n)
                                             + heuristic_function(n, Node(problem.goal)))
        astar_results_file.write("heuristic cost: " + str(heuristic_function(Node(problem.start_state),
                                                      Node(problem.goal))) + ", actual cost: " + str(cost) + "\n")
        # We want to draw solution maps only for 10 problems as required.
        if counter < 10:
            draw_solution_map(path)
        counter += 1
    astar_results_file.close()


# Compute the runtime of AStar algorithm for 100 problems.
@tools.timed
def astar_runtime():
    arbitrary_solvable_problems = get_100_solvable_search_problems()
    for problem in arbitrary_solvable_problems:
        source = problem[0]
        target = problem[1]
        problem = RoutingProblem(source, target, MapData.get_instance())
        best_first_graph_search(problem, cost_function, f=lambda n: g(n)
                                             + heuristic_function(n, Node(problem.goal)))


# Write in results/IDAStarRuns.txt the costs and the heuristic evaluations
# (from a start state to a goal state) of the 5 problems according to IDAStar algorithm.
def idastar_solution_for_5_problems():
    astar_results_file = open('results/IDAStarRuns.txt', "w")
    problems_list = load_data()
    for line in range(0, 5):
        source = problems_list[line][0]
        target = problems_list[line][1]
        problem = RoutingProblem(int(source), int(target), MapData.get_instance())
        path = idastar(problem)
        cost = 0
        for i in range(len(path) - 1):
            links = MapData.get_instance().get(path[i]).links
            for link in links:
                if link.target == path[i+1]:
                    cost += cost_function(link)
                    break
        astar_results_file.write("heuristic cost: " + str(heuristic_function(Node(problem.start_state),
                                                          Node(problem.goal))) + ", actual cost: " + str(cost) + "\n")
    astar_results_file.close()


# Compute the runtime of IDAstar algorithm for 100 problems.
@tools.timed
def idastar_runtime():
    arbitrary_solvable_problems = get_100_solvable_search_problems()
    for i in range(0, 5):
        source = arbitrary_solvable_problems[i][0]
        target = arbitrary_solvable_problems[i][1]
        problem = RoutingProblem(source, target, MapData.get_instance())
        idastar(problem)


# Draw a graph which its x axis is the heuristic time evaluation and its y axis is the actual time.
def draw_graph():
    x, y = [], []
    # Read the results of AStar from results/AStarRuns.txt.
    with open('results/AStarRuns.txt', 'r') as f:
        for line in f:
            split_line = line.split(',')
            x.append(float(split_line[0].split(' ')[2]))
            y.append(float(split_line[1].split(' ')[3]))
    p.axis([-0.01, 0.2, -0.01, 0.2], witdh=50)  # Set the positions of the axes.
    p.title("A-Star Costs", fontsize=25, color=(0.2, 0.75, 0.5))  # Set the title of the graph.
    p.xlabel("Heuristic cost", fontsize=13, color=(0.2, 0.75, 0.5))  # Set the label of x-axis.
    p.ylabel("Actual cost", fontsize=13, color=(0.2, 0.75, 0.5))   # Set the label of y-axis.
    p.scatter(x, y, s=25, marker="*", color=(0.2, 0.75, 0.5), )  # Scatter the (x,y) points at their locations.
    p.show()  # Show the graph.


# Draw a map of A* solution.
def draw_solution_map(path):
    # Get all the roads from MapData.
    roads = MapData.get_instance()
    # Clear the current figure.
    p.clf()
    source_lon_values, source_lat_values, target_lon_values, target_lat_values = [], [], [], []
    for source, target in zip(path[:-1], path[1:]):
        s, t = roads[source], roads[target]
        source_lon_values.append(s.lon)
        source_lat_values.append(s.lat)
        target_lon_values.append(t.lon)
        target_lat_values.append(t.lat)
    # Plot the data.
    p.plot(source_lon_values, source_lat_values, target_lon_values, target_lat_values, color=(0.2, 0.75, 0.5))
    solutions_file_name = 'solutions_img/from_' + str(path[0]) + '_to_' + str(path[len(path) - 1]) + '.png'
    # Save the figure in the specified file name.
    p.savefig(solutions_file_name, bbox_inches='tight')


# write_problems_in_csv()
# ucs_solution_for_100_problems()
# ucs_runtime()
# astar_solution_for_100_problems()
# draw_graph()
# astar_runtime()
# idastar_solution_for_5_problems()
# idastar_runtime()