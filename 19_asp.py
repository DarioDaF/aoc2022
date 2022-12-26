
from utils import readInput, defaultdict, dataclass, parseClingo
import argparse, regex, time
import subprocess as sp

ap = argparse.ArgumentParser()
ap.add_argument('--test', action='store_true', help='use test input')
ap.add_argument('--part2', action='store_true', help='solve part 2')
args = ap.parse_args()

if args.test:
    text = '''Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
'''
else:
    text = readInput()

# Problem relevant classes

class MyPool:
    ...
class MyPool(defaultdict[str, int]):
    def __init__(self, __map = {}):
        super().__init__(int, __map)
    def __add__(self, other: MyPool):
        res = MyPool(self)
        for k, v in other.items():
            res[k] += v
        return res
    def __iadd__(self, other: MyPool):
        for k, v in other.items():
            self[k] += v
        return self
    def __sub__(self, other: MyPool):
        res = MyPool(self)
        for k, v in other.items():
            res[k] -= v
        return res
    def __isub__(self, other: MyPool):
        for k, v in other.items():
            self[k] -= v
        return self
    def __neg__(self):
        res = MyPool((k, -v) for k, v in self)
        return res
    def __contains__(self, other):
        if isinstance(other, MyPool):
            for k, v in other.items():
                if (k not in self) or (v > self[k]):
                    return False
            return True
        else:
            return super().__contains__(other)
    def __repr__(self):
        return 'MyPool(' + dict.__repr__(self) + ')'

@dataclass
class Recipe:
    produces: MyPool # Robots
    costs: MyPool

@dataclass
class Blueprint:
    id: int
    recipes: list[Recipe]
    def possibleRecipes(self, resources: MyPool):
        return (recipe for recipe in self.recipes if recipe.costs in resources)

class Game:
    def __init__(self, blueprint: Blueprint, start_robot_pool: MyPool):
        self.blueprint = blueprint
        self.robot_pool = MyPool(start_robot_pool)
        self.robot_construction_pool = MyPool()
        self.resources = MyPool()
        self.t = 0
    def tick(self):
        self.resources += self.robot_pool
        self.robot_pool += self.robot_construction_pool
        self.robot_construction_pool = MyPool()
        self.t += 1
    def useRecipe(self, recipe: Recipe|int):
        if isinstance(recipe, int):
            recipe = self.blueprint.recipes[recipe]
        assert recipe.costs in self.resources
        self.resources -= recipe.costs
        self.robot_construction_pool += recipe.produces
    def possibleRecipes(self):
        return self.blueprint.possibleRecipes(self.resources)
    def __repr__(self):
        return f'''Game(blueprint={self.blueprint.id}) @ {self.t}:
  Robots: {self.robot_pool}
  Resources: {self.resources}
  Robots in construction: {self.robot_construction_pool}
'''

# Defines

TARGET = 'geode'
START_ROBOT_POOL = { 'ore': 1 }
TIME = 32 if args.part2 else 24

# Read file

blueprints: dict[int, Blueprint] = {}

r_bp = regex.compile('^Blueprint (\d+): ')
r_act = regex.compile('Each (\w+) robot costs(?: (?:and )?(\d+) (\w+))+\.')
for line in text.strip().split('\n'):
    id = int(r_bp.match(line).groups()[0])
    blueprint = Blueprint(id, [])
    for find in r_act.finditer(line):
        captures = find.allcaptures()
        produces = MyPool({ captures[1][0]: 1 })
        costs = MyPool({ o: int(i) for i, o in zip(captures[2], captures[3]) })
        blueprint.recipes.append(Recipe(produces, costs))
    blueprints[id] = blueprint
    if args.part2 and id >= 3:
        break

# Part 2

# Do real stuff

tot = 1 if args.part2 else 0
for bid, blueprint in blueprints.items():
    print(f'Blueprint {bid}:')
    t0 = time.monotonic()
    print('  Generating model...')
    # Core
    model = '''

time(0.._time).

material_opt(nothing).
material_opt(M) :- material(M).

resource(0, M, 0) :- material(M).

% Complete robots at 0
r0abs(MAT) :- robot(0, MAT, I), I != 0.
robot(0, MAT, 0) :- not r0abs(MAT), material(MAT).

% Complete recipe_costs
rcabs(MATR, MAT) :- recipe_cost(MATR, MAT, I), I != 0.
recipe_cost(MATR, MAT, 0) :- not rcabs(MATR, MAT), material_opt(MATR), material(MAT).

robot(TIME, MAT, I+1) :- robot(TIME-1, MAT, I),
    build_robot(TIME-1, MAT).
robot(TIME, MAT, I) :- robot(TIME-1, MAT, I),
    not build_robot(TIME-1, MAT),
    time(TIME). % Need a cap

resource_after_consume(TIME, MAT, I-IC) :- resource(TIME, MAT, I),
    build_robot(TIME, MATR), % consume resource the same tick you create a robot
    recipe_cost(MATR, MAT, IC).

resource(TIME, MAT, I+IR) :- resource_after_consume(TIME-1, MAT, I),
    robot(TIME-1, MAT, IR).

{ build_robot(TIME, MAT) : material_opt(MAT) } = 1 :- time(TIME).

:- resource_after_consume(_, _, I), I < 0.
#maximize { I : resource(_time, _target, I) }.

end_resource(MAT, I) :- resource(_time, MAT, I).
#show build_robot/2.
#show end_resource/2.

'''
    # Data
    model += f'''
% Blueprint {bid}
#const _time = {TIME}.
#const _target = {TARGET}.
'''
    for item, count in START_ROBOT_POOL.items():
        model += f'robot(0, {item}, {count}).\n'
    mats = set()
    for i, recipe in enumerate(blueprint.recipes):
        produces = 'nothing'
        for item, count in recipe.produces.items():
            assert produces == 'nothing'
            assert count == 1
            produces = item
        assert produces not in mats
        mats.add(produces)
        model += f'material({produces}).\n'
        for item, count in recipe.costs.items():
            model += f'recipe_cost({produces}, {item}, {count}).\n'
    print('  Running model')
    p = sp.run(['clingo'], input=model, capture_output=True, encoding='utf-8')
    t1 = time.monotonic()

    res_type, preds = parseClingo(p.stdout)
    
    print(f'  {res_type} in {t1 - t0} s')
    for pred, pargs in preds:
        if pred == 'end_resource' and pargs[0] == TARGET:
            n_targets = int(pargs[1])
            print(f'  Built {n_targets} targets')
            break
    if args.part2:
        tot *= n_targets
    else:
        tot += bid * n_targets

print(f'\nResult: {tot}')
