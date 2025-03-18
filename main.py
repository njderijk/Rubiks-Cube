import json
import os.path
import random

import Cube
from solver import IDA_star, build_heuristic_db

def scramble_cube_string():
    cube_string = "WWWWWWWWWYYYYYYYYYOOOOOOOOORRRRRRRRRGGGGGGGGGBBBBBBBBB"
    scrambled = list(cube_string)
    random.shuffle(scrambled)
    return "".join(scrambled)

cube = Cube.Rubiks("WWWWWWWWWYYYYYYYYYOOOOOOOOORRRRRRRRRGGGGGGGGGBBBBBBBBB")
# cube.scramble(1)

MAX_MOVES = 6
NEW_HEURISTICS = False
HEURISTIC_FILE = 'heuristic.json'

moves = ["move_F"
"move_F_prime",
"move_B",
"move_B_prime",
"move_L",
"move_L_prime",
"move_T",
"move_T_prime",
"move_R",
"move_R_prime",
"move_D",
"move_D_prime"]

if os.path.exists(HEURISTIC_FILE):
    with open(HEURISTIC_FILE) as f:
        h_db = json.load(f)
else:
    h_db = None

if h_db is None or NEW_HEURISTICS is True:
    actions = cube.moves
    h_db = build_heuristic_db(
        cube.stringify(),
        actions,
        max_moves = MAX_MOVES,
        heuristic = h_db
    )

    with open(HEURISTIC_FILE, 'w', encoding='utf-8') as f:
        json.dump(
            h_db,
            f,
            ensure_ascii=False,
            indent=4
        )
#--------------------------------
print('----------')
cube.scramble(1)

# cube = Cube.Rubiks(scramble_cube_string())

# for i in range (0,12):
#     cube.random_move()


Cube.printRubiks(cube)
print('----------')
#--------------------------------

solver = IDA_star(h_db)
print("\n** Running Solver **\n")
moves = solver.run(cube.stringify())
print(moves)

for m in moves:
    if m == "move_F":
        cube.move_F()
    elif m == "move_F_prime":
        cube.move_F_prime()
    elif m == "move_B":
        cube.move_B()
    elif m == "move_B_prime":
        cube.move_B_prime()
    elif m == "move_L":
        cube.move_L()
    elif m == "move_L_prime":
        cube.move_L_prime()
    elif m == "move_T":
        cube.move_T()
    elif m == "move_T_prime":
        cube.move_T_prime()
    elif m == "move_R":
        cube.move_R()
    elif m == "move_R_prime":
        cube.move_R_prime()
    elif m == "move_D":
        cube.move_D()
    elif m == "move_D_prime":
        cube.move_D_prime()

    # if m[0] == 'h':
    #     cube.horizontal_twist(m[1], m[2])
    # elif m[0] == 'v':
    #     cube.vertical_twist(m[1], m[2])
    # elif m[0] == 's':
    #     cube.side_twist(m[1], m[2])



Cube.printRubiks(cube)