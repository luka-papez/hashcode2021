from typing import FrozenSet, List, Dict, NamedTuple, Tuple

'''
    Types
'''
PizzaIndex = int
Ingredient = str

class Pizza(NamedTuple):
    idx: PizzaIndex
    ingredients: FrozenSet[Ingredient]

PizzaInventory = List[Pizza]

TeamSizes = Dict[int, int]

TeamDelivery = List[PizzaIndex]

Solution = List[TeamDelivery]

'''
    Algorithm
'''
def simple_solver(team_sizes: TeamSizes, inventory: PizzaInventory) -> Solution:
    '''
        For each team
            choose the next available pizzas and deliver it to them
    '''
    deliveries: List[TeamDelivery] = []

    while team_sizes:
        chosen_team_size = max(team_sizes)  # picking team from largest to smallest makes a difference of about 3 million points

        pizza_indices = [pizza.idx for pizza in inventory[:chosen_team_size]]

        if len(pizza_indices) != chosen_team_size:
            break
        deliveries.append(pizza_indices)

        inventory = inventory[chosen_team_size:]

        team_sizes[chosen_team_size] -= 1
        if team_sizes[chosen_team_size] == 0:
            del team_sizes[chosen_team_size]

    return deliveries

'''
    IO
'''
def parse_input(filepath: str) -> Tuple[TeamSizes, PizzaInventory]:
    def read_file_lines(filepath: str) -> List[str]:
        with open(filepath ) as f:
            return list(map(str.strip, f.readlines()))

    teams, *pizzas = read_file_lines(filepath)

    _, *team_sizes = map(int, teams.split())

    inventory: PizzaInventory = []
    for i, pizza_desc in enumerate(pizzas):
        _, *ingredients_list = pizza_desc.split()

        pizza = Pizza(i, frozenset(ingredients_list))

        inventory.append(pizza)

    return dict(zip([2, 3, 4], team_sizes)), inventory

def format_solution(team_deliveries: Solution) -> str:
    lines = []

    lines.append(str(len(solution)))

    for pizza_indices in team_deliveries:
        lines.append(
            '{} {}'.format(
                len(pizza_indices),
                ' '.join(map(str, pizza_indices))
            )
        )

    return '\n'.join(lines)

'''
    Runner
'''
inputs = [
    ('A', '/Users/lukapapez/Downloads/a_example'),
    ('B', '/Users/lukapapez/Downloads/b_little_bit_of_everything.in'),
    ('C', '/Users/lukapapez/Downloads/c_many_ingredients.in'),
    ('D', '/Users/lukapapez/Downloads/d_many_pizzas.in'),
    ('E', '/Users/lukapapez/Downloads/e_many_teams.in')
]

for letter, input_filepath in inputs:
    team_sizes, pizza_inventory = parse_input(input_filepath)

    solution = simple_solver(team_sizes, pizza_inventory)

    print('solved', input_filepath)

    with open(letter + '.solution', 'w+') as f:
        print(format_solution(solution), file=f)

# zip practice.py utils.py source.zip
