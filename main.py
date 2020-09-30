'''
Parse input and run appropriate code.
We just parse input and call methods from other modules.
'''

import zipfile
# Import search_algorithms module and call the appropriate functions.
import search_algorithms


def find_ucs_route(source, target):
    return search_algorithms.find_ucs_route(source, target)


def find_astar_route(source, target):
    return search_algorithms.find_astar_route(source, target)


def find_idastar_route(source, target):
    return search_algorithms.find_idastar_route(source, target)
    

def dispatch(argv):
    from sys import argv
    source, target = int(argv[2]), int(argv[3])
    if argv[1] == 'ucs':
        path = find_ucs_route(source, target)
    elif argv[1] == 'astar':
        path = find_astar_route(source, target)
    elif argv[1] == 'idastar':
        path = find_idastar_route(source, target)
    print(' '.join(str(j) for j in path))


if __name__ == '__main__':
    with zipfile.ZipFile("db\israel.zip", "r") as zip_ref:
        zip_ref.extractall("db")
    from sys import argv
    dispatch(argv)
