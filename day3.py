"""
--- Day 3: Crossed Wires ---

The gravity assist was successful, and you're well on your way to the Venus refuelling station. During the rush back on Earth, the fuel management system wasn't completely installed, so that's next on the priority list.

Opening the front panel reveals a jumble of wires. Specifically, two wires are connected to a central port and extend outward on a grid. You trace the path each wire takes as it leaves the central port, one wire per line of text (your puzzle input).

The wires twist and turn, but the two wires occasionally cross paths. To fix the circuit, you need to find the intersection point closest to the central port. Because the wires are on a grid, use the Manhattan distance for this measurement. While the wires do technically cross right at the central port where they both start, this point does not count, nor does a wire count as crossing with itself.

For example, if the first wire's path is R8,U5,L5,D3, then starting from the central port (o), it goes right 8, up 5, left 5, and finally down 3:

...........
...........
...........
....+----+.
....|....|.
....|....|.
....|....|.
.........|.
.o-------+.
...........

Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down 4, and left 4:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........

These wires cross at two locations (marked X), but the lower-left one is closer to the central port: its distance is 3 + 3 = 6.

Here are a few more examples:

    R75,D30,R83,U83,L12,D49,R71,U7,L72
    U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
    R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
    U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135

What is the Manhattan distance from the central port to the closest intersection?

"""
from dataclasses import dataclass
from collections import defaultdict

with open("input/day3.txt") as input_file:
    inp = input_file.readlines()

line_1 = inp[0].strip().split(",")
line_2 = inp[1].strip().split(",")

# sample inputs from the story
SAMPLE1 = "R8,U5,L5,D3".split(",")
SAMPLE2 = "U7,R6,D4,L4".split(",")
SAMPLE_1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72".split(",")
SAMPLE_2 = "U62,R66,U55,R34,D71,R55,D58,R83".split(",")

# probably not needed, but maybe for part 2; a small coordinate class for clarity
@dataclass 
class Coordinate:
    x: int
    y: int


# parse all steps first, finding their points on the grid, then jam them in sets and finally together to find the intersections
def calculate_intersections(line1, line2):
    line_1_x, line_1_y, line_2_x, line_2_y = 0, 0, 0, 0
    line_1_coords = set()
    line_2_coords = set()

    for step in line1:
        position = Coordinate(line_1_x, line_1_y)
        direction, length = step[0], int(step[1:])
        if direction == "L":
            line_1_x -= length
            for i in range(line_1_x, position.x):
                line_1_coords.add((i, line_1_y))
        elif direction == "R":
            line_1_x += length
            for i in range(position.x, line_1_x+1):
                line_1_coords.add((i, line_1_y))
        elif direction == "U":
            line_1_y += length
            for i in range(position.y, line_1_y+1):
                line_1_coords.add((line_1_x, i))
        elif direction == "D":
            line_1_y -= length
            for i in range(line_1_y, position.y):
                line_1_coords.add((line_1_x, i))

    for step in line2:
        position = Coordinate(line_2_x, line_2_y)
        direction, length = step[0], int(step[1:])
        if direction == "L":
            line_2_x -= length
            for i in range(line_2_x, position.x):
                line_2_coords.add((i, line_2_y))
        elif direction == "R":
            line_2_x += length
            for i in range(position.x, line_2_x+1):
                line_2_coords.add((i, line_2_y))
        elif direction == "U":
            line_2_y += length
            for i in range(position.y, line_2_y+1):
                line_2_coords.add((line_2_x, i))
        elif direction == "D":
            line_2_y -= length
            for i in range(line_2_y, position.y):
                line_2_coords.add((line_2_x, i))

    return line_1_coords.intersection(line_2_coords)


def shortest_manhattan_distance(intersections):
    shortest = 1000000
    for item in intersections:
        if item[0] != 0 and item[1] != 0:
            manhattan = abs(item[0]) + abs(item[1])
            shortest = min(shortest, manhattan)
    return shortest

assert shortest_manhattan_distance(calculate_intersections(SAMPLE_1, SAMPLE_2)) == 159

print(shortest_manhattan_distance(calculate_intersections(line_1, line_2)))

"""
--- Part Two ---

It turns out that this circuit is very timing-sensitive; you actually need to minimize the signal delay.

To do this, calculate the number of steps each wire takes to reach each intersection; choose the intersection where the sum of both wires' steps is lowest. If a wire visits a position on the grid multiple times, use the steps value from the first time it visits that position when calculating the total value of a specific intersection.

The number of steps a wire takes is the total number of grid squares the wire has entered to get to that location, including the intersection being considered. Again consider the example from above:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........

In the above example, the intersection closest to the central port is reached after 8+5+5+2 = 20 steps by the first wire and 7+6+4+3 = 20 steps by the second wire for a total of 20+20 = 40 steps.

However, the top-right intersection is better: the first wire takes only 8+5+2 = 15 and the second wire takes only 7+6+2 = 15, a total of 15+15 = 30 steps.

Here are the best steps for the extra examples from above:

    R75,D30,R83,U83,L12,D49,R71,U7,L72
    U62,R66,U55,R34,D71,R55,D58,R83 = 610 steps
    R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
    U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = 410 steps

What is the fewest combined steps the wires must take to reach an intersection?
"""

# So for part 2, we need to keep track of both the coordinates of the intersections as well as the number to steps to get there.
# I'll simply use a dict for that with {coord: steps}
# Unfortunately because going left or down is "stepping backwards" through the grid, I had to change a looot of the loop code.

def calculate_intersections_counting_steps(line1, line2):
    line_1_x, line_1_y, line_2_x, line_2_y = 0, 0, 0, 0
    line_1_coords = {(0,0): 0}
    line_2_coords = {(0,0): 0}
    step = 0
    for item in line1:
        position = Coordinate(line_1_x, line_1_y)
        direction, length = item[0], int(item[1:])
        if direction == "L":
            line_1_x -= length
            for i in range(position.x-1, line_1_x-1, -1):
                step += 1
                if (i, line_1_y) not in line_1_coords:
                    line_1_coords[(i, line_1_y)] = step
                
        elif direction == "R":
            line_1_x += length
            for i in range(position.x+1, line_1_x+1):
                step += 1
                if (i, line_1_y) not in line_1_coords:
                    line_1_coords[(i, line_1_y)] = step

        elif direction == "U":
            line_1_y += length
            for i in range(position.y+1, line_1_y+1):
                step += 1
                if (line_1_x, i) not in line_1_coords:
                    line_1_coords[line_1_x, i] = step

        elif direction == "D":
            line_1_y -= length
            for i in range(position.y-1, line_1_y-1, -1):
                # print(line_1_x, i)
                step += 1
                if (line_1_x, i) not in line_1_coords:
                    line_1_coords[line_1_x, i] = step
    
    # reset step count for the 2nd line
    step = 0

    for item in line2:
        position = Coordinate(line_2_x, line_2_y)
        direction, length = item[0], int(item[1:])
        if direction == "L":
            line_2_x -= length
            for i in range(position.x-1, line_2_x-1, -1):
                step += 1
                if (i, line_2_y) not in line_2_coords:
                    line_2_coords[(i, line_2_y)] = step
                
        elif direction == "R":
            line_2_x += length
            for i in range(position.x+1, line_2_x+1):
                step += 1
                if (i, line_2_y) not in line_2_coords:
                    line_2_coords[(i, line_2_y)] = step

        elif direction == "U":
            line_2_y += length
            for i in range(position.y+1, line_2_y+1):
                step += 1
                if (line_2_x, i) not in line_2_coords:
                    line_2_coords[line_2_x, i] = step
                    
        elif direction == "D":
            line_2_y -= length
            for i in range(position.y-1, line_2_y-1, -1):
                step += 1
                if (line_2_x, i) not in line_2_coords:
                    line_2_coords[line_2_x, i] = step

    # check total steps for every intersection, then return smallest
    intersections = dict()
    for k, v in line_1_coords.items():
        if k in line_2_coords and k != (0,0):
            intersections[k] = v + line_2_coords[k]
    return min(intersections.values())

assert calculate_intersections_counting_steps(SAMPLE_1, SAMPLE_2) == 610
print(calculate_intersections_counting_steps(line_1, line_2))