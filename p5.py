import sys, parse, random
import time, os, copy

def print_layout(layout):
    res = ""
    for row in layout:
        res+="".join(row)
        res+="\n"
    return res

def generate_choices(layout, loc, player):
    choices = []
    r, c = loc
    ghost_valid = set(["P", ".", " "])
    if player == 'P':
        if layout[r][c+1] != "%": choices.append(("E",(r,c+1)))
        if layout[r-1][c] != "%": choices.append(("N",(r-1,c)))
        if layout[r+1][c] != "%": choices.append(("S",(r+1,c)))
        if layout[r][c-1] != "%": choices.append(("W",(r,c-1)))
    else: 
        if layout[r][c+1] in ghost_valid: choices.append(("E",(r,c+1)))
        if layout[r-1][c] in ghost_valid: choices.append(("N",(r-1,c)))
        if layout[r+1][c] in ghost_valid: choices.append(("S",(r+1,c)))
        if layout[r][c-1] in ghost_valid: choices.append(("W",(r,c-1)))
    return choices

def eval_fun(choice_, layout, players, score, cur_player, food_greed=1):

    food = players["food"]
    eval_max = -float("inf")
    food_min_dist = float("inf")
    cur = players["P"]
    dir, choice = choice_
    if cur_player != "P":
        gh_sq = (players[cur_player][0]-cur[0])**2 + (players[cur_player][1]-cur[1])**2
        gh_abs = abs(players[cur_player][0]-cur[0]) + abs(players[cur_player][1]-cur[1])
        return 0.5*gh_sq + 0.5*gh_abs #+score
    for i in range(len(food)):
        cur_dist = 0.5*(abs(food[i][0]-cur[0]) + abs(food[i][1]-cur[1])) + 0.5*((food[i][0]-cur[0])**2 + (food[i][1]-cur[1])**2)
        if cur_dist < food_min_dist:
            food_min = food[i]
            food_min_dist = cur_dist
    food_dist = 0.5*(abs(food_min[0]-choice[0])+abs(food_min[1]-choice[1])) + 0.5*((food_min[0]-choice[0])**2+(food_min[1]-choice[1])**2)
    # print(f"{food_dist}")
    # if cur_player != "P":
    #     return food_greed/(food_dist+1) + abs(players[cur_player][0]-players["P"][0]) + abs(players[cur_player][1]-players["P"][1]) #+score

    ghost_min_dist = float("inf")
    ghosts = ["W", "X", "Y", "Z"][:len(players)-2]
    for i in range(len(ghosts)):
        cur_dist = 0.5*(abs(players[ghosts[i]][0]-cur[0]) + abs(players[ghosts[i]][1]-cur[1])) + 0.5*((players[ghosts[i]][0]-cur[0])**2 + (players[ghosts[i]][1]-cur[1])**2)
        if cur_dist < ghost_min_dist:
            ghost_min = ghosts[i]
            ghost_min_dist = cur_dist
    
    ghost_dist = 0.5*((players[ghost_min][0]-choice[0])**2+(players[ghost_min][1]-choice[1])**2) + 0.5*(abs(players[ghost_min][0]-choice[0])+abs(players[ghost_min][1]-choice[1]))
    if ghost_dist > 1 and food_dist == 1: eval_cur = sys.maxsize
    eval_cur = food_greed/(food_dist+0.1) + ghost_dist
    return eval_cur #+score


###START here
def terminal_test(players):
    food = players["food"]
    if len(food) == 0: return True
    ghost_count = len(players) - 2
    ghosts = ["W", "X", "Y", "Z"]
    for i in range(ghost_count):
        if players["P"] == players[ghosts[i]]: return True
    return False

def utility(players, turns, food_init_count, score):
    
    score=0
    food = players["food"]
    player_count = len(players) - 1
    number_of_pacman_moves = turns//player_count + 1
    score += -number_of_pacman_moves + 10*(food_init_count-len(food))
    if len(food) == 0: score= sys.maxsize #score=float("inf")
    for player in players:
        if player not in ["food", "P"]: 
            if players["P"] == players[player]: score=-sys.maxsize #score=-float("inf")
    return score

def min_value(layout, players, tot_depth, k, food_init_count, score, choice, cur, test):
    food = players["food"]
    ghost_count = len(players) - 2
    ghosts = ["W", "X", "Y", "Z"][:ghost_count]
    player = cur
    player_order = ['P'] + ghosts
    cur_player_index = player_order.index(player)
    next_player_index = (cur_player_index + 1) % len(player_order)
    next_player = player_order[next_player_index]

    #base case 1: terminal state
    if terminal_test(players): return utility(players, tot_depth, food_init_count, score), None, None
    # if terminal_test(players): return eval_fun(choice, layout, players, score, player), None, None
    #base case 2: depth-limt reached
    elif tot_depth/(len(players)-1) >= k: return eval_fun(choice, layout, players, score, player), None, None
    v = float('inf')
    v_arg = v_choice = None

    for choice in generate_choices(layout, players[player], player):
        #updating layout and player locations
        updated_layout = copy.deepcopy(layout)
        updated_players = copy.deepcopy(players)
        cur_loc = players[player]
        updated_layout[cur_loc[0]][cur_loc[1]] = " "
        dir, choice_ = choice
        updated_players[player] = choice_
        updated_layout[choice_[0]][choice_[1]] = player

        #updating food
        # for i in range(len(updated_players["food"])):
        #     if updated_players["food"][i] == choice_: 
        #         updated_players["food"].pop(i)
        #         break

        # if (cur_pos+tot_depth)%(len(players)-1) == 0:
        if player == ghosts[-1]:
            v_new, _, _ = max_value(updated_layout, updated_players, tot_depth+1, k, food_init_count, score, choice, next_player, test)
            if v_new < v:
                v = v_new
                v_arg = dir
                v_choice = choice_
        else:
            v_new, _, _ = min_value(updated_layout, updated_players, tot_depth+1, k, food_init_count, score, choice, next_player, test)
            # print(v_new)
            if v_new < v:
                v = v_new
                v_arg = dir
                v_choice = choice_
    # print(f"{player, test}")
    return v, v_arg, v_choice

def max_value(layout, players, tot_depth, k, food_init_count, score, choice, cur, test):
    food = players["food"]
    ghost_count = len(players) - 2
    ghosts = ["W", "X", "Y", "Z"][:ghost_count]
    player = cur
    player_order = ['P'] + ghosts
    cur_player_index = player_order.index(player)
    next_player_index = (cur_player_index + 1) % len(player_order)
    next_player = player_order[next_player_index]

    #base case 1: terminal state
    if terminal_test(players): return utility(players, tot_depth, food_init_count, score), None, None
    # if terminal_test(players): return eval_fun(choice, layout, players, score, player), None, None
    #base case 2: depth-limt reached
    elif tot_depth/(len(players)-1) >= k: return eval_fun(choice, layout, players, score, player), None, None
    v = -float('inf')
    v_arg = v_choice = None

    for choice in generate_choices(layout, players[player], player):
        #updating layout and player locations
        updated_layout = copy.deepcopy(layout)
        updated_players = copy.deepcopy(players)
        cur_loc = players[player]
        updated_layout[cur_loc[0]][cur_loc[1]] = " "
        dir, choice_ = choice
        updated_players[player] = choice_
        updated_layout[choice_[0]][choice_[1]] = player

        #updating food
        # for i in range(len(updated_players["food"])):
        #     if updated_players["food"][i] == choice_: 
        #         updated_players["food"].pop(i)
        #         break

        # if (cur_pos+tot_depth)%(len(players)-1) == 0:
        if player == ghosts[-1]:
            v_new, _, _ = max_value(updated_layout, updated_players, tot_depth+1, k, food_init_count, score, choice, next_player, test)
            if v_new > v:
                v = v_new
                v_arg = dir
                v_choice = choice_
        else:
            v_new, _, _ = min_value(updated_layout, updated_players, tot_depth+1, k, food_init_count, score, choice, next_player, test)
            # print(v_new)
            if v_new > v:
                v = v_new
                v_arg = dir
                v_choice = choice_
    # print(f"{player, test}")
    return v, v_arg, v_choice

def min_max_multiple_ghosts(problem, k):
    #Your p5 code here
    seed, layout, players = problem
    food = players['food']
    random.seed(seed, version=1)
    turn = 1
    score = 0
    solution = ''
    

    solution += f"seed: {seed}\n"
    solution += str(score) + "\n"
    solution += print_layout(layout)

    player_count = len(players)-1
    player_list = ["P","W", "X", "Y", "Z"][:player_count]
    flag_overlap_ghost_food = [(False, ("F", "F"))]*(player_count-1)
    food_init_count = len(food)

    while 1:
        # print(print_layout(layout))
        #determine which player moves
        # print(score)
        player = player_list[(turn%player_count) -1]
        
        #remove player that is moving
        layout[players[player][0]][players[player][1]] = " " 
        
        #determine player's next move
        player_loc = players[player]
        choices = generate_choices(layout, player_loc, player)
        
        #calculate index for flag_overlap_ghost_food
        flag_overlap_ghost_food_index = (turn%player_count-2) if (turn%player_count-2) != -2 else -1

        #when ghost can not move
        if len(choices) == 0:
            layout[players[player][0]][players[player][1]] = player
            solution += f"{turn}: {player} moving \n"
            solution += print_layout(layout) + "score: " + str(score) + "\n" 
            turn += 1
            continue
        cur_pos = player_list.index(player)
        #selecting next direction to move 
        if player == "P": util, direction, new_player_loc = max_value(layout, players, 0, k, food_init_count, score, None, player, player)
        else: 
            util, direction, new_player_loc = min_value(layout, players, 0, k, food_init_count, score, None, player, player)
        # print(f"{new_player_loc, direction}")
        players[player] = new_player_loc
        # if player == "P": print(players["W"])
        # print(new_player_loc)
        solution += f"{turn}: {player} moving {direction}\n"
        print(f"{turn}: {player} moving {direction}")
        if player == "P": score -= 1
        else:
            # print(f"{flag_overlap_ghost_food_index}{player}")
            if flag_overlap_ghost_food[flag_overlap_ghost_food_index][0]:
                layout[flag_overlap_ghost_food[flag_overlap_ghost_food_index][1][0]][flag_overlap_ghost_food[flag_overlap_ghost_food_index][1][1]] = "."
                flag_overlap_ghost_food[flag_overlap_ghost_food_index] = (False, ("F", "F"))

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

                #finding ghost that ate the player
                for gh in player_list[1:]:
                    if players[gh] == (players['P'][0],players['P'][1]): layout[players['P'][0]][players['P'][1]] = gh       
                
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
                        flag_overlap_ghost_food[flag_overlap_ghost_food_index] = (True, (food[i][0],food[i][1]))
                        break
            else:
                score -= 500
                layout[players['P'][0]][players['P'][1]] = player
                solution += print_layout(layout) + "score: " + str(score) + "\n"
                solution += "WIN: Ghost"
                return solution, "Ghost"
        print(print_layout(layout))
        solution += print_layout(layout) + "score: " + str(score) + "\n" 
        turn += 1
        
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 5
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    k = int(sys.argv[2])
    num_trials = int(sys.argv[3])
    verbose = bool(int(sys.argv[4]))
    print('test_case_id:',test_case_id)
    print('k:',k)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = min_max_multiple_ghosts(copy.deepcopy(problem), k)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)