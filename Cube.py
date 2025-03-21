import numpy as np
import random
import itertools
import copy
import timeit

solved_string = "WWWWWWWWWYYYYYYYYYOOOOOOOOORRRRRRRRRGGGGGGGGGBBBBBBBBB"

def printRubiks(rubiks):
    print(  "            ", rubiks.faces['B'][0][0], rubiks.faces['B'][1][0], rubiks.faces['B'][2][0] + "\n", 
        "           ", rubiks.faces['B'][3][0], rubiks.faces['B'][4][0], rubiks.faces['B'][5][0] + "\n", 
        "           ", rubiks.faces['B'][6][0], rubiks.faces['B'][7][0], rubiks.faces['B'][8][0] + "\n\n", 

        rubiks.faces['L'][0][0], rubiks.faces['L'][1][0], rubiks.faces['L'][2][0], "     ", rubiks.faces['D'][0][0], rubiks.faces['D'][1][0], rubiks.faces['D'][2][0], "     ", rubiks.faces['R'][0][0], rubiks.faces['R'][1][0], rubiks.faces['R'][2][0],  "     ", rubiks.faces['T'][0][0], rubiks.faces['T'][1][0], rubiks.faces['T'][2][0], "\n", 
        rubiks.faces['L'][3][0], rubiks.faces['L'][4][0], rubiks.faces['L'][5][0], "     ", rubiks.faces['D'][3][0], rubiks.faces['D'][4][0], rubiks.faces['D'][5][0], "     ", rubiks.faces['R'][3][0], rubiks.faces['R'][4][0], rubiks.faces['R'][5][0],  "     ", rubiks.faces['T'][3][0], rubiks.faces['T'][4][0], rubiks.faces['T'][5][0], "\n", 
        rubiks.faces['L'][6][0], rubiks.faces['L'][7][0], rubiks.faces['L'][8][0], "     ", rubiks.faces['D'][6][0], rubiks.faces['D'][7][0], rubiks.faces['D'][8][0], "     ", rubiks.faces['R'][6][0], rubiks.faces['R'][7][0], rubiks.faces['R'][8][0],  "     ", rubiks.faces['T'][6][0], rubiks.faces['T'][7][0], rubiks.faces['T'][8][0], "\n\n", 

        "           ", rubiks.faces['F'][0][0], rubiks.faces['F'][1][0], rubiks.faces['F'][2][0], "\n",
        "           ", rubiks.faces['F'][3][0], rubiks.faces['F'][4][0], rubiks.faces['F'][5][0], "\n",
        "           ", rubiks.faces['F'][6][0], rubiks.faces['F'][7][0], rubiks.faces['F'][8][0], "\n\n"
)
    
class Rubiks:
    def __init__(self, state):
        if len(state) != 54:
            raise ValueError("Invalid cube state: must be a 54-character string.")

        self.previous_state = ''
        self.best_score = 0

        self.completed = ''
        
        self.faces = {
            'F': list(state[0:9]),   # Front
            'B': list(state[9:18]),  # Back
            'L': list(state[18:27]), # Left
            'R': list(state[27:36]), # Right
            'T': list(state[36:45]), # Top
            'D': list(state[45:54])  # Down/Bottom
        }

        self.moves = [
            self.move_T, self.move_T_prime, 
            self.move_D, self.move_D_prime, 
            self.move_F, self.move_F_prime, 
            self.move_B, self.move_B_prime, 
            self.move_L, self.move_L_prime, 
            self.move_R, self.move_R_prime
        ]

    def random_move(self):
        action = random.choice(self.moves)
        print("executing random move: " + action.__name__)
        self = action()
        return self
    
    def reset_state(self, action):
        action()
        action()
        action()

    def scramble(self, n):
        combined_lists = list(itertools.chain(self.faces['F'] + self.faces['B'] + self.faces['L'] + self.faces['R'] + self.faces['T'] +  self.faces['D']))
        
        for i in range (0, n):
            random.shuffle(combined_lists)

        self.faces = {
            'F': list(combined_lists[0:9]),   # Front
            'B': list(combined_lists[9:18]),  # Back
            'L': list(combined_lists[18:27]), # Left
            'R': list(combined_lists[27:36]), # Right
            'T': list(combined_lists[36:45]), # Top
            'D': list(combined_lists[45:54])  # Down/Bottom
        }

    def save(self):
        new_s = copy.deepcopy(self)
        return new_s

    def load_prev(self):
        self = self.previous_state

    def stringify(self):
        return ''.join(list(itertools.chain(self.faces['F'] + self.faces['B'] + self.faces['L'] + self.faces['R'] + self.faces['T'] +  self.faces['D'])))
        # return ''.join(            
        #     self.faces['F'][0:9],
        #     )

    def look_move_ahead(self):
        for action in self.moves:
            action()
            score = (10 * self.count_completed_faces() ) + 2 * self.count_correct_pieces()  # Weighted score
            if score > self.best_score:
                self.reset_state(action)
                action()
                return action
            else:
                self.look_move_ahead()

        # for action in self.moves:
        #     # print("No better move found. Identify best move with best future potential")
            
        #     scores = []
        #     actions = []

        #     for first_action in self.moves:
        #         first_action() # No action helped in a n=1 look-ahead, so perform each action and then look at consequences
                
        #         score = (10 * self.count_completed_faces() ) + 2 * self.count_correct_pieces()  # Weighted score
                
        #         if score > self.best_score:
        #                 self.reset_state(first_action)
        #                 first_action()
        #                 return first_action
        #         for second_action in self.moves:
        #             second_action()
        #             if self.checkCompletion() == True:
        #                 bestAction = first_action # Because you need to do the first action to get to this point
        #                 # self.reset_state(second_action)
        #                 return bestAction

        #             score = (10 * self.count_completed_faces() ) + 2 * self.count_correct_pieces()  # Weighted score
                    
        #             if score > self.best_score:
        #                 self.reset_state(second_action)
        #                 self.reset_state(first_action)
        #                 first_action()
        #                 return first_action
        #             else:
        #                 # print("Recursived.")
        #                 self.look_move_ahead()

    def check_best_next_move(self, sides, num_pieces):
        save_state = self.save()

        bestAction = None       

        actions = []
        scores = []

        for action in self.moves:
            action()
            # print("Rubiks after performed action...")
            # printRubiks(self)
            # self.checkCompletion()
            if self.checkCompletion() == True:
                # self.reset_state(action)
                return action
            else:
                score = (10 * self.count_completed_faces() ) + 2 * self.count_correct_pieces()  # Weighted score
                scores.append(score)
                actions.append(action)
                self.reset_state(action)

        # print(scores)
        # print(np.argmax(scores))
        # print("Best action = ", actions[np.argmax(scores)])        
        # print("***\nBest action = ", actions[np.argmax(scores)], "\nBest action reward = ", max(scores), "\n***")

        bestAction = actions[np.argmax(scores)]

        # If the best action improves the current position, accept it as the NBM
        if max(scores) > self.best_score:
            self.best_score = max(scores)
            bestAction = action
            self = save_state
            # self.reset_state(action)
            bestAction()
            return bestAction

        
        # If not, look one move further (make this a function in the future so we can continuously look one move further)
        else:
            # print("No better move found. Identify best move with best future potential")
            
            scores = []
            actions = []
            for first_action in self.moves:
                first_action() # No action helped in a n=1 look-ahead, so perform each action and then look at consequences
                for second_action in self.moves:
                    second_action()
                    if self.checkCompletion() == True:
                        bestAction = first_action # Because you need to do the first action to get to this point
                        # self.reset_state(second_action)
                        return bestAction

                    score = (10 * self.count_completed_faces() ) + 2 * self.count_correct_pieces()  # Weighted score
                    scores.append(score)

                    actions.append(first_action) # We add the max scores of the second move to the first move to traverse forwards. Because a first move is needed to get to the second
                    # After scores are calculated, reset the states so next actions can be checked

                    self.reset_state(second_action)
                self.reset_state(first_action)
            
            bestAction = actions[np.argmax(scores)]
            if max(scores) > self.best_score:
                self.best_score = max(scores)
                bestAction = action
                bestAction()
                return bestAction
            else:
                bestAction() # Then just go with the best action
                return bestAction

        # print(bestAction, "Reward = ", reward, "\n", "New completed faces = ", new_state.count_completed_faces(), "\n", "New correct pieces = " , new_state.count_correct_pieces())
        # print(self.best_score)
        
        # self.reset_state(action)

    def checkCompletion(self):
        # Check if every side contains only one color
        if len(list(set(list(self.faces['F'])))) == 1 & len(list(set(list(self.faces['L'])))) == 1 & len(list(set(list(self.faces['B'])))) == 1 & len(list(set(list(self.faces['R'])))) == 1 & len(list(set(list(self.faces['D'])))) == 1 & len(list(set(list(self.faces['T'])))) == 1:
            print("\n***\nRubiks completed!\n***\n")
            self.completed = True
            return True
        else:
            self.completed = False
            return False
        
    def count_completed_faces(self):
        return sum(1 for face in self.faces.values() if all(c == face[0] for c in face))
    
    def count_correct_pieces(self):
        return sum(sum(1 for c in face if c == face[4]) - 1 for face in self.faces.values())
        
    def rotate_face(self, face):
        self.faces[face] = [
            self.faces[face][6], self.faces[face][3], self.faces[face][0],
            self.faces[face][7], self.faces[face][4], self.faces[face][1],
            self.faces[face][8], self.faces[face][5], self.faces[face][2]
        ]
    
    def move_T(self):
        self.rotate_face('T')
        temp = self.faces['F'][:3]
        self.faces['F'][:3] = self.faces['R'][:3]
        self.faces['R'][:3] = self.faces['B'][:3]
        self.faces['B'][:3] = self.faces['L'][:3]
        self.faces['L'][:3] = temp
    
    def move_T_prime(self): # Move CCW
        for _ in range(3):
            self.move_T()
    
    def move_D(self):
        self.rotate_face('D')
        temp = self.faces['F'][6:]
        self.faces['F'][6:] = self.faces['L'][6:]
        self.faces['L'][6:] = self.faces['B'][6:]
        self.faces['B'][6:] = self.faces['R'][6:]
        self.faces['R'][6:] = temp
    
    def move_D_prime(self): # Move CCW
        for _ in range(3):
            self.move_D()
    
    def move_R(self):
        self.rotate_face('R')
        temp = [self.faces['T'][2], self.faces['T'][5], self.faces['T'][8]]
        self.faces['T'][2], self.faces['T'][5], self.faces['T'][8] = self.faces['F'][2], self.faces['F'][5], self.faces['F'][8]
        self.faces['F'][2], self.faces['F'][5], self.faces['F'][8] = self.faces['D'][2], self.faces['D'][5], self.faces['D'][8]
        self.faces['D'][2], self.faces['D'][5], self.faces['D'][8] = self.faces['B'][6], self.faces['B'][3], self.faces['B'][0]
        self.faces['B'][6], self.faces['B'][3], self.faces['B'][0] = temp
    
    def move_R_prime(self): # Move CCW
        for _ in range(3):
            self.move_R()
    
    def move_L(self):
        self.rotate_face('L')
        temp = [self.faces['T'][0], self.faces['T'][3], self.faces['T'][6]]
        self.faces['T'][0], self.faces['T'][3], self.faces['T'][6] = self.faces['B'][8], self.faces['B'][5], self.faces['B'][2]
        self.faces['B'][8], self.faces['B'][5], self.faces['B'][2] = self.faces['D'][0], self.faces['D'][3], self.faces['D'][6]
        self.faces['D'][0], self.faces['D'][3], self.faces['D'][6] = self.faces['F'][0], self.faces['F'][3], self.faces['F'][6]
        self.faces['F'][0], self.faces['F'][3], self.faces['F'][6] = temp
    
    def move_L_prime(self): # Move CCW
        for _ in range(3):
            self.move_L()
    
    def move_F(self):
        self.rotate_face('F')
        temp = [self.faces['T'][6], self.faces['T'][7], self.faces['T'][8]]
        self.faces['T'][6], self.faces['T'][7], self.faces['T'][8] = self.faces['L'][8], self.faces['L'][5], self.faces['L'][2]
        self.faces['L'][8], self.faces['L'][5], self.faces['L'][2] = self.faces['D'][2], self.faces['D'][1], self.faces['D'][0]
        self.faces['D'][2], self.faces['D'][1], self.faces['D'][0] = self.faces['R'][0], self.faces['R'][3], self.faces['R'][6]
        self.faces['R'][0], self.faces['R'][3], self.faces['R'][6] = temp
    
    def move_F_prime(self): # Move CCW
        for _ in range(3):
            self.move_F()
    
    def move_B(self):
        self.rotate_face('B')
        temp = [self.faces['T'][0], self.faces['T'][1], self.faces['T'][2]]
        self.faces['T'][0], self.faces['T'][1], self.faces['T'][2] = self.faces['R'][8], self.faces['R'][5], self.faces['R'][2]
        self.faces['R'][8], self.faces['R'][5], self.faces['R'][2] = self.faces['D'][8], self.faces['D'][7], self.faces['D'][6]
        self.faces['D'][8], self.faces['D'][7], self.faces['D'][6] = self.faces['L'][0], self.faces['L'][3], self.faces['L'][6]
        self.faces['L'][0], self.faces['L'][3], self.faces['L'][6] = temp
    
    def move_B_prime(self): # Move CCW
        for _ in range(3):
            self.move_B()


# cube = Rubiks("WWWWWWWWWYYYYYYYYYOOOOOOOOORRRRRRRRRGGGGGGGGGBBBBBBBBB")

# print(cube.stringify())
# # cube.move_B()
# # cube.move_D_prime()
# # cube.move_L_prime()
# # cube.move_F_prime()

# # printRubiks(cube)
# # cube.checkCompletion()
# cube.scramble(1)

# x = cube.count_completed_faces()
# y = cube.count_correct_pieces()
# print("Completed faces =", x , "\n"
#         "Completed pieces = ", y, "\n")

# cube.best_score = (5 * cube.count_completed_faces() ) + 2 * cube.count_correct_pieces()  # Weighted score

# Completed = False
# max_moves = 1
# moves = 0


# print("*** Starting Rubiks ***\n")
# printRubiks(cube)
# print("*** Starting Rubiks ***\n")

# cube.completed = cube.checkCompletion()

# print("*** Starting score ***\n", str(cube.best_score))
# while cube.completed == False:
#     print("\nMove #", moves + 1, "\n")

#     cube.check_best_next_move(x, y)
#     print("New score = ", str(cube.best_score))

#     x = cube.count_completed_faces()
#     y = cube.count_correct_pieces()
#     print("Completed faces =", x , "\n"
#           "Completed pieces = ", y, "\n")

#     moves = moves + 1

#     # print(cube.checkCompletion())
#     # cube.checkCompletion()

#     if cube.completed == True:
#         print("***\nSolving COMPLETED!\n***\n Rubiks cube solved in", str(moves), " moves.")
#         break

#     elif cube.completed == False:
#         if moves >= max_moves:
#             print("Solving FALED. Could not solve cube in", str(moves), "moves.")
#             printRubiks(cube)
#             break
#         else:
#             continue
        