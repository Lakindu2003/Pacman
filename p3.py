import sys, grader, parse, math, random

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

def random_play_multiple_ghosts(problem):
    #Your p3 code here
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

    while 1:
        #determine which player moves
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

        #selecting next direction to move 
        direction ,new_player_loc = random.choice(choices)
        players[player] = new_player_loc

        solution += f"{turn}: {player} moving {direction}\n"
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
                            return solution
                        break
            else: 
                score -= 500

                #finding ghost that ate the player
                for gh in player_list[1:]:
                    if players[gh] == (players['P'][0],players['P'][1]): layout[players['P'][0]][players['P'][1]] = gh       
                
                solution += print_layout(layout) + "score: " + str(score) + "\n"
                solution += "WIN: Ghost"
                return solution
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
                return solution
        
        solution += print_layout(layout) + "score: " + str(score) + "\n" 
        turn += 1
        
    return solution


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, random_play_multiple_ghosts, parse.read_layout_problem)