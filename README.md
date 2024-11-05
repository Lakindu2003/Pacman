# Pacman
## Files
- parse.py: Input parser
- p1.py: Random pacman vs 1 random ghost
- p2.py: Pacman vs 1 random ghost
- p3.py: Random pacman vs 2-4 random ghosts
- p4.py: Pacman vs 2-4 random ghosts
- **p5.py: Minimax pacman vs 2-4 minimax ghosts**
- **p6.py: Expectimax pacman vs 2-4 random ghosts**

## Key Features
- Evaluation function
    * Pacman: food_greed/(distance_to_closest_food+constant) + distance_to_closest_ghost
    * Ghost: 0.5*distance_to_pacman
- Distance metrics
    * p1.py, p2.py, p3.py, p4.py and p6.py: Manhattan distance
    * p5.py: 0.5\*Manhattan_distance + 0.5\*euclidean_distance
- Depth-limited search: Limit depth of expectimax and minimax trees to k (function input).
- Algorithms
    * Classic minimax algorithm
    * Classic expectimax algorithm
