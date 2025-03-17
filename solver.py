from Cube import Rubiks
from random import randint, choice
import tqdm

moves = [
    "move_F",
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
    "move_D_prime"
    ]

class IDA_star(object):
    def __init__(self, heuristic, max_depth = 20):
        """
        Input: heuristic - dictionary representing the heuristic pre computed map
               max_depth - integer representing the max depth you want your game tree to reach (default = 20) [OPTIONAL]
        Description: Initialize the solver
        Output: None
        """
        self.max_depth = max_depth
        self.threshold = max_depth
        self.min_threshold = None
        self.heuristic = heuristic
        self.moves = []

    def run(self, state):
        """
        Input: state - string representing the current state of the cube
        Description: solve the rubix cube
        Output: list containing the moves taken to solve the cube
        """
        while True:
            status = self.search(state, 1)
            if status: return self.moves
            self.moves = []
            self.threshold = self.min_threshold
        return []

    def search(self, state, g_score):
        """
        Input: state - string representing the current state of the cube
               g_score - integer representing the cost to reach the current node
        Description: search the game tree using the IDA* algorithm
        Output: boolean representing if the cube has been solved
        """
        cube = Rubiks(state=state)
        if cube.checkCompletion():
            return True
        elif len(self.moves) >= self.threshold:
            return False
        min_val = float('inf')
        best_action = None
        for a in moves:
            cube = Rubiks(state=state)
            # print("X", a)
            if a == "move_F":
                cube.move_F()
            elif a == "move_F_prime":
                cube.move_F_prime()
            elif a == "move_B":
                cube.move_B()
            elif a == "move_B_prime":
                cube.move_B_prime()
            elif a == "move_L":
                cube.move_L()
            elif a == "move_L_prime":
                cube.move_L_prime()
            elif a == "move_T":
                cube.move_T()
            elif a == "move_T_prime":
                cube.move_T_prime()
            elif a == "move_R":
                cube.move_R()
            elif a == "move_R_prime":
                cube.move_R_prime()
            elif a == "move_D":
                cube.move_D()
            elif a == "move_D_prime":
                cube.move_D_prime()

            # self.moves.append(a)

            if cube.checkCompletion():
                self.moves.append(a)
                return True
            
            cube_str = cube.stringify()
            h_score = self.heuristic[cube_str] if cube_str in self.heuristic else self.max_depth
            f_score = g_score + h_score
            if f_score < min_val:
                min_val = f_score
                best_action = [(cube_str, a)]
            elif f_score == min_val:
                if best_action is None:
                    best_action = [(cube_str, a)]
                else:
                    best_action.append((cube_str, a))
        if best_action is not None:
            if self.min_threshold is None or min_val < self.min_threshold:
                self.min_threshold = min_val
            next_action = choice(best_action)
            self.moves.append(next_action[1])
            status = self.search(next_action[0], g_score + min_val)
            if status: return status
        return False

def build_heuristic_db(state, actions, max_moves = 20, heuristic = None):
    """
    Input: state - string representing the current state of the cube
           actions -list containing tuples representing the possible actions that can be taken
           max_moves - integer representing the max amount of moves alowed (default = 20) [OPTIONAL]
           heuristic - dictionary containing current heuristic map (default = None) [OPTIONAL]
    Description: create a heuristic map for determining the best path for solving a rubiks cube
    Output: dictionary containing the heuristic map
    """
    if heuristic is None:
        heuristic = {state: 0}
    que = [(state, 0)]
    node_count = sum([len(actions) ** (x + 1) for x in range(max_moves + 1)])
    with tqdm.tqdm(total=node_count, desc='Heuristic DB') as pbar:
        while True:
            if not que:
                break
            s, d = que.pop()
            if d > max_moves:
                continue
            for a in moves:
                cube = Rubiks(state=s)
                # print(a)
                if a == "move_F":
                     cube.move_F()
                elif a == "move_F_prime":
                    cube.move_F_prime()
                elif a == "move_B":
                    cube.move_B()
                elif a == "move_B_prime":
                    cube.move_B_prime()
                elif a == "move_L":
                    cube.move_L()
                elif a == "move_L_prime":
                    cube.move_L_prime()
                elif a == "move_T":
                    cube.move_T()
                elif a == "move_T_prime":
                    cube.move_T_prime()
                elif a == "move_R":
                    cube.move_R()
                elif a == "move_R_prime":
                    cube.move_R_prime()
                elif a == "move_D":
                    cube.move_D()
                elif a == "move_D_prime":
                    cube.move_D_prime()
                # if a[0] == 'h':
                #     cube.horizontal_twist(a[1], a[2])
                # elif a[0] == 'v':
                #     cube.vertical_twist(a[1], a[2])
                # elif a[0] == 's':
                #     cube.side_twist(a[1], a[2])
                # print(cube.stringify())
                a_str = cube.stringify()
                if a_str not in heuristic or heuristic[a_str] > d + 1:
                    heuristic[a_str] = d + 1
                que.append((a_str, d+1))
                pbar.update(1)
    return heuristic

