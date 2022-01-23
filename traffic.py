from typing import NamedTuple, List, Sequence, Tuple, Set, Dict

from collections import defaultdict

from operator import itemgetter

from random import randint

'''
    Types
'''
# input related
Duration = int
Intersection = int
StreetName = str
class Street(NamedTuple):
    begin: Intersection
    end: Intersection
    length: int
Map = Dict[StreetName, Street]
CarPath = List[StreetName]
Traffic = List[CarPath]

# solution related
class GreenLight(NamedTuple):
    street: StreetName
    seconds: int
class LightPattern(NamedTuple):
    intersection: Intersection
    green_light_sequence: List[GreenLight]
Solution = List[LightPattern]

'''
    IO
'''
def load_input(filepath: str) -> Tuple[Duration, Map, Traffic]:
    with open(filepath) as f:
        lines = list(map(str.strip, f.readlines()))

    duration, num_intersections, num_streets, num_cars, car_score = map(int, lines[0].split())

    lines = lines[1:]
    street_strs = lines[:num_streets]
    streets: Map = {}
    for street_str in street_strs:
        begin_str, end_str, name, length = street_str.split()
        streets[name] = Street(int(begin_str), int(end_str), int(length))

    lines = lines[num_streets:]
    cars_strs = lines[:num_cars]
    traffic: Traffic = []
    for car_str in cars_strs:
        _, *car_path = car_str.split()
        traffic.append(car_path)

    return duration, streets, traffic

def format_solution(solution: Solution) -> str:
    lines: List[str] = []

    lines.append(str(len(solution)))

    for light_pattern in solution:
        lines.append(str(light_pattern.intersection))
        lines.append(str(len(light_pattern.green_light_sequence)))

        for green_light in light_pattern.green_light_sequence:
            lines.append(f'{green_light.street} {green_light.seconds}')

    return '\n'.join(lines)

'''
    Algorithm
'''
def solver_1(duration: Duration, city: Map, traffic: Traffic) -> Solution:
    '''
        Finds a car that can make it to the destination and makes a chain of green lights for that car.
    '''
    solution = []

    for car_path in traffic:
        if len(car_path) <= duration:
            for street_name in car_path:
                solution.append(
                    LightPattern(
                        city[street_name].end,
                        [GreenLight(street_name, 1)]
                    )
                )
            break
    else:
        raise RuntimeError('no car can make it to its destination in time!')

    return solution

def solver_2(duration: Duration, city: Map, traffic: Traffic) -> Solution:
    '''
        On each intersection, turn on each of its lights one by one.
        Each light is green for one second.
    '''

    intersection_incoming_streets: Dict[int, Set[StreetName]] = defaultdict(set)
    #intersection_outgoing_streets: Dict[int, Set[StreetName]] = defaultdict(set)

    for street_name, street in city.items():
        intersection_incoming_streets[street.end].add(street_name)
        #intersection_outgoing_streets[street.begin].add(street_name)

    solution = []
    for intersection, incoming_streets in intersection_incoming_streets.items():
        sequence = []
        for incoming_street in incoming_streets:
            sequence.append(
                GreenLight(
                    incoming_street,
                    1
                )
            )

        solution.append(
            LightPattern(
                intersection,
                sequence
            )
        )

    return solution


def solver_3(simulation_duration: Duration, city: Map, traffic: Traffic) -> Solution:
    '''
        On each intersection, turn on each of its lights one by one.
        Each light is green for enough time so that all initially queued cars may pass.
        Don't open the streets in which no one wants to go initially.
    '''
    num_paths_street_is_found: Dict[StreetName, int] = defaultdict(int)
    for car_path in traffic:
        for street_name in car_path:
            num_paths_street_is_found[street_name] += 1

    intersection_incoming_streets: Dict[int, Set[StreetName]] = defaultdict(set)
    #intersection_outgoing_streets: Dict[int, Set[StreetName]] = defaultdict(set)

    for street_name, street in city.items():
        intersection_incoming_streets[street.end].add(street_name)
        #intersection_outgoing_streets[street.begin].add(street_name)

    solution = []
    for intersection, incoming_streets in intersection_incoming_streets.items():
        sequence = []
        for incoming_street in incoming_streets:
            street_business = num_paths_street_is_found[incoming_street]
            if not street_business:
                continue

            sequence.append(
                GreenLight(
                    incoming_street,
                    max(street_business, 1)
                )
            )

        if not sequence:
            continue

        solution.append(
            LightPattern(
                intersection,
                sequence
            )
        )

    return solution

def solver_4(simulation_duration: Duration, city: Map, traffic: Traffic) -> Solution:
    '''
        On each intersection, turn on each of its lights one by one.
        Each light is green proportional to how busy the street initially is.
        Also open the streets in which no one wants to go initially for 1 second.
    '''
    num_paths_street_is_found: Dict[StreetName, int] = defaultdict(int)
    for car_path in traffic:
        for street_name in car_path:
            num_paths_street_is_found[street_name] += 1

    intersection_incoming_streets: Dict[int, Set[StreetName]] = defaultdict(set)
    #intersection_outgoing_streets: Dict[int, Set[StreetName]] = defaultdict(set)

    for street_name, street in city.items():
        intersection_incoming_streets[street.end].add(street_name)
        #intersection_outgoing_streets[street.begin].add(street_name)

    solution = []
    for intersection, incoming_streets in intersection_incoming_streets.items():
        sequence = []
        for incoming_street in incoming_streets:
            street_business = num_paths_street_is_found[incoming_street]
            if not street_business:
                continue

            sequence.append(
                GreenLight(
                    incoming_street,
                    max(street_business, 1)
                )
            )

        if not sequence:
            continue

        min_light_seconds = min(green_light.seconds for green_light in sequence)
        sequence = [
            green_light._replace(seconds=green_light.seconds // min_light_seconds) for green_light in sequence
        ]

        solution.append(
            LightPattern(
                intersection,
                sequence
            )
        )

    return solution

def solver_5(simulation_duration: Duration, city: Map, traffic: Traffic) -> Solution:
    '''
        Similar to solver 3.
        On each intersection, turn on each of its lights one by one.
        Each light is green for a random amount of time between 1 and 5 seconds.
        Don't open the streets in which no one wants to go initially.
    '''
    num_paths_street_is_found: Dict[StreetName, int] = defaultdict(int)
    for car_path in traffic:
        for street_name in car_path:
            num_paths_street_is_found[street_name] += 1

    intersection_streets: Dict[int, Set[StreetName]] = defaultdict(set)

    for street_name, street in city.items():
        intersection_streets[street.end].add(street_name)

    solution = []
    for intersection, streets in intersection_streets.items():
        sequence = []
        for incoming_street in streets:
            street_business = num_paths_street_is_found[incoming_street]
            if not street_business:
                continue

            sequence.append(
                GreenLight(
                    incoming_street,
                    randint(1, 5)
                )
            )

        if not sequence:
            continue

        solution.append(
            LightPattern(
                intersection,
                sequence
            )
        )

    return solution

'''
    Runner
'''
inputs = [
    ('a', 'inputs/a.txt'),
    ('b', 'inputs/b.txt'),
    ('c', 'inputs/c.txt'),
    ('d', 'inputs/d.txt'),
    ('e', 'inputs/e.txt'),
    ('f', 'inputs/f.txt'),
]

for letter, filepath in inputs:
    puzzle_input = load_input(filepath)

    #solution = solver_1(*puzzle_input) # ~20k points
    #solution = solver_2(*puzzle_input) # ~7.9M points
    #solution = solver_3(*puzzle_input) # ~8.5M points
    #solution = solver_4(*puzzle_input) # ~8.5M points
    solution = solver_5(*puzzle_input) # ~9.0M points

    #print(*solution, sep='\n')

    with open(letter + '.solution', 'w+') as f:
        print(format_solution(solution), file=f)
