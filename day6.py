r"""
--- Day 6: Universal Orbit Map ---

You've landed at the Universal Orbit Map facility on Mercury. Because navigation in space often involves transferring between orbits, the orbit maps here are useful for finding efficient routes between, for example, you and Santa. You download a map of the local orbits (your puzzle input).

Except for the universal Center of Mass (COM), every object in space is in orbit around exactly one other object. An orbit looks roughly like this:

                  \
                   \
                    |
                    |
AAA--> o            o <--BBB
                    |
                    |
                   /
                  /

In this diagram, the object BBB is in orbit around AAA. The path that BBB takes around AAA (drawn with lines) is only partly shown. In the map data, this orbital relationship is written AAA)BBB, which means "BBB is in orbit around AAA".

Before you use your map data to plot a course, you need to make sure it wasn't corrupted during the download. To verify maps, the Universal Orbit Map facility uses orbit count checksums - the total number of direct orbits (like the one shown above) and indirect orbits.

Whenever A orbits B and B orbits C, then A indirectly orbits C. This chain can be any number of objects long: if A orbits B, B orbits C, and C orbits D, then A indirectly orbits D.

For example, suppose you have the following map:

COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L

Visually, the above map of orbits looks like this:

        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I

In this visual representation, when two objects are connected by a line, the one on the right directly orbits the one on the left.

Here, we can count the total number of orbits as follows:

    D directly orbits C and indirectly orbits B and COM, a total of 3 orbits.
    L directly orbits K and indirectly orbits J, E, D, C, B, and COM, a total of 7 orbits.
    COM orbits nothing.

The total number of direct and indirect orbits in this example is 42.

What is the total number of direct and indirect orbits in your map data?
"""
import pprint
from collections import defaultdict

SAMPLE_INPUT = """
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
""".split("\n")[1:-1]

# part 1: First experiment a bit with input parsing
# I want some sort of dict to keep track of objects in relation to the objects they orbit
def parse_input(lines):
    galaxy = defaultdict(list)
    for line in lines:
        orbiting, obj = line.strip().split(")")
        galaxy[obj].append(orbiting)
    return galaxy


# the total direct & indirect orbits is similar to a search tree; it's a recursive problem, since an object is not only orbited by other objects, but also by their other orbiting objects.
def count_total_orbits(obj, galaxy, count=0):
    # We've reached an 'outer' object that has no other objects orbited by it
    # print(f"Counting {obj} at count {count}")
    if obj not in galaxy:
        return count
    else:
        # print(f"Counting {galaxy[obj]}")
        count += len(galaxy[obj])
        # traverse the object's orbited objects, counting each
        return sum([count_total_orbits(orb, galaxy, count) for orb in galaxy[obj]])

def total_count(galaxy):
    return sum([count_total_orbits(obj, galaxy) for obj in galaxy])


sample_galaxy = parse_input(SAMPLE_INPUT)
assert total_count(sample_galaxy) == 42
print(sample_galaxy)
with open("input/day6.txt") as input_file:
    inp = input_file.readlines()

galaxy = parse_input(inp)
print(total_count(galaxy))

"""
--- Part Two ---

Now, you just need to figure out how many orbital transfers you (YOU) need to take to get to Santa (SAN).

You start at the object YOU are orbiting; your destination is the object SAN is orbiting. An orbital transfer lets you move from any object to an object orbiting or orbited by that object.

For example, suppose you have the following map:

COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN

Visually, the above map of orbits looks like this:

                          YOU
                         /
        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I - SAN

In this example, YOU are in orbit around K, and SAN is in orbit around I. To move from K to I, a minimum of 4 orbital transfers are required:

    K to J
    J to E
    E to D
    D to I

Afterward, the map of orbits looks like this:

        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I - SAN
                 \
                  YOU

What is the minimum number of orbital transfers required to move from the object YOU are orbiting to the object SAN is orbiting? (Between the objects they are orbiting - not between YOU and SAN.)
"""

# part 2: edit the sample galaxy first to match the examples given
sample_galaxy["YOU"] = ["K"]
sample_galaxy["SAN"] = ["I"]

# now we could implement some sort of cost function to calculate the minimum transfer; every transfer costs 1.
# But before that we need to know how to transfer first. That is difficult because transfering can go forwards or backwards.
# Fortunately there's an easier way:
# Since it's a pure binary tree we can simple let both santa & you travel backwards to a common point, and find the sum of the distance they travelled


# Calculate route to the beginning storing all points
def travel_back(a, galaxy, route=[]):
    if a in galaxy:
        route.append(a)
        return travel_back(galaxy[a][0], galaxy, route)
    else:
        return route

# Get distance to the first intersection of you & santa's routes
def find_closest_intersection(route1, route2):
    all_intersections = [r for r in route1 if r in route2] 
    return sum([route1.index(all_intersections[0]), route2.index(all_intersections[0])]) - 2

your_route = (travel_back("YOU", sample_galaxy, []))
santa_route = (travel_back("SAN", sample_galaxy, []))
print(find_closest_intersection(your_route, santa_route))

your_route2 = (travel_back("YOU", galaxy, []))
santa_route2 = (travel_back("SAN", galaxy, []))
print(find_closest_intersection(your_route2, santa_route2))
