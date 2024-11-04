import os, sys
def read_layout_problem(file_path):
    #Your p1 code here
    layout = []
    players = dict()
    players['food'] = []
    other = set(["%", " "])
    with open(file_path, 'r') as file:
        line_number = -1
        for line in file:
            if line_number == -1:
                seed = int(line.split()[1])
                line_number+=1
                continue
            new_line = []
            char_number = 0
            for char in line:
                if char in other:
                    new_line.append(char)
                elif char == '\n':
                    None 
                elif char == ".":
                    new_line.append(char)
                    players['food'].append((line_number, char_number))
                else:
                    players[char] = (line_number, char_number)
                    new_line.append(char)
                char_number += 1
            line_number += 1
            layout.append(new_line)
    if seed == -1: seed = None
    problem = (seed, layout, players)
    return problem

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        problem = read_layout_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')