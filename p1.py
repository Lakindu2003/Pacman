import sys, random, grader, parse

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

def random_play_single_ghost(problem):
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
        direction ,new_player_loc = random.choice(choices)
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
                            return solution
                        break
            else: 
                score -= 500
                layout[players['P'][0]][players['P'][1]] = "W"
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
                        flag_overlap_ghost_food = (True, (food[i][0],food[i][1]))
                        break
            else:
                score -= 500
                layout[players['P'][0]][players['P'][1]] = "W"
                solution += print_layout(layout) + "score: " + str(score) + "\n"
                solution += "WIN: Ghost"
                return solution
        
        solution += print_layout(layout) + "score: " + str(score) + "\n" 
        turn += 1
        
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, random_play_single_ghost, parse.read_layout_problem)