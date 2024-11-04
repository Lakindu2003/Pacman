import sys, parse, random
import time, os, copy
from collections import deque

def print_layout(layout):
    res = ""
    for row in layout:
        res+="".join(row)
        res+="\n"
    return res

def generate_choices(layout, loc):
    choices = []
    r, c = loc
    #when there are more ghosts, have to modify the selection for ghosts
    if layout[r][c+1] != "%": choices.append(("E",(r,c+1)))
    if layout[r-1][c] != "%": choices.append(("N",(r-1,c)))
    if layout[r+1][c] != "%": choices.append(("S",(r+1,c)))
    if layout[r][c-1] != "%": choices.append(("W",(r,c-1)))
    return choices

def eval_fun(choices, layout, food, players, food_greed=1):
    eval_max = -float("inf")
    food_min_dist = float("inf")
    cur = players["P"]
    for i in range(len(food)):
        cur_dist = abs(food[i][0]-cur[0]) + abs(food[i][1]-cur[1])
        if cur_dist < food_min_dist:
            food_min = food[i]
            food_min_dist = cur_dist
    
    for i in range(len(choices)):
        dir, choice = choices[i]
        food_dist = abs(food_min[0]-choice[0])+abs(food_min[1]-choice[1])
        ghost_dist = abs(players["W"][0]-choice[0])+abs(players["W"][1]-choice[1])
        
        if food_dist == 0 and ghost_dist > 1: 
            return dir, choice
        # elif food_dist < ghost_dist + 2 and food_dist < 3: return dir, choice
        elif food_dist == 0: continue

        eval_cur = food_greed/(food_dist) + ghost_dist
        if eval_cur > eval_max:
            eval_max = eval_cur
            direction = dir
            new_player_loc = choice

    return direction, new_player_loc

def better_play_single_ghosts(problem):
    #Your p1 code here
    seed, layout, players = problem
    food = players['food']
    random.seed(seed, version=1)
    turn = 1
    score = 0
    solution = ''
    flag_overlap_ghost_food = (False, ("F", "F"))

    solution += f"seed: {seed}\n"
    solution += str(score) + "\n"
    solution += print_layout(layout)

    while 1:
        #determine which player moves
        if turn % 2: player = 'P'
        else: player = 'W'
        
        #remove player that is moving
        layout[players[player][0]][players[player][1]] = " " 
        
        #determine player's next move
        player_loc = players[player]
        choices = generate_choices(layout, player_loc)
        if player == "W": direction, new_player_loc = random.choice(choices)
        else: 
            direction, new_player_loc = eval_fun(choices, layout, food, players, food_greed=1)
        
        players[player] = new_player_loc
        
        #checking for interactions
        solution += f"{turn}: {player} moving {direction}\n"
        if player == "P": score -= 1
        else:
            if flag_overlap_ghost_food[0]:
                layout[flag_overlap_ghost_food[1][0]][flag_overlap_ghost_food[1][1]] = "."
                flag_overlap_ghost_food = (False, ("F", "F"))

        if player == 'P':
            if layout[new_player_loc[0]][new_player_loc[1]] == " ":
                layout[new_player_loc[0]][new_player_loc[1]] = player 
            elif layout[new_player_loc[0]][new_player_loc[1]] == ".":
                for i in range(len(food)):
                    if food[i] == new_player_loc:
                        layout[food[i][0]][food[i][1]] = "P"
                        food.pop(i)
                        score += 10
                        if not len(food):
                            score += 500
                            solution += print_layout(layout) + "score: " + str(score) + "\n"
                            solution += "WIN: Pacman"
                            return solution, "Pacman"
                        break
            else: 
                score -= 500
                layout[players['P'][0]][players['P'][1]] = "W"
                solution += print_layout(layout) + "score: " + str(score) + "\n"
                solution += "WIN: Ghost"
                return solution, "Ghost"
        else:
            if layout[new_player_loc[0]][new_player_loc[1]] == " ":
                layout[new_player_loc[0]][new_player_loc[1]] = player 
            elif layout[new_player_loc[0]][new_player_loc[1]] == ".":
                for i in range(len(food)):
                    if food[i] == new_player_loc:
                        layout[food[i][0]][food[i][1]] = player
                        flag_overlap_ghost_food = (True, (food[i][0],food[i][1]))
                        break
            else:
                score -= 500
                layout[players['P'][0]][players['P'][1]] = "W"
                solution += print_layout(layout) + "score: " + str(score) + "\n"
                solution += "WIN: Ghost"
                return solution, "Ghost"
        
        solution += print_layout(layout) + "score: " + str(score) + "\n" 
        turn += 1
    winner = 'Ghost'
    return solution, winner

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 2
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    num_trials = int(sys.argv[2])
    verbose = bool(int(sys.argv[3]))
    print('test_case_id:',test_case_id)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = better_play_single_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)