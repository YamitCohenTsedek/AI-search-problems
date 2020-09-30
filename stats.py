'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''

from collections import namedtuple
from ways import load_map_from_csv
import sys
import collections


def map_statistics(roads):
    # Return a dictionary containing the desired information.
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])
    num_of_junctions = len(roads)
    num_of_links = 0
    max_branching_factor = 0
    min_branching_factor = sys.maxsize
    max_distance = 0
    min_distance = sys.maxsize
    sum_of_distances = 0
    link_types_list = []
    # Find the maximal and the minimal branching factor for all the junctions.
    for junction in roads.junctions():
        if len(junction.links) > max_branching_factor:
            max_branching_factor = len(junction.links)
        elif len(junction.links) < min_branching_factor:
            min_branching_factor = len(junction.links)
    for link in roads.iterlinks():
        num_of_links += 1
        link_types_list.append(link.highway_type)
        sum_of_distances = sum_of_distances + link.distance
        if link.distance > max_distance:
            max_distance = link.distance
        elif link.distance < min_distance:
            min_distance = link.distance
    link_type_histogram = collections.Counter(link_types_list)

    return {
        'Number of junctions': num_of_junctions,
        'Number of links': num_of_links,
        'Outgoing branching factor': Stat(max=max_branching_factor, min=min_branching_factor, avg=float(num_of_links)/num_of_junctions),
        'Link distance': Stat(max=max_distance, min=min_distance, avg=float(sum_of_distances)/num_of_links),
        # Value should be a dictionary.
        # Mapping each road_info.TYPE to the no' of links of this type.
        'Link type histogram': link_type_histogram, 
    }


def print_stats():
    for k, v in map_statistics(load_map_from_csv()).items():
        print('{}: {}'.format(k, v))

        
if __name__ == '__main__':
    from sys import argv
    assert len(argv) == 1
    print_stats()
