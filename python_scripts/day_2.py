from collections import defaultdict
import time
from tqdm import tqdm

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

# Define when player won the game
win_conditions = {"A": "Y", "B": "Z", "C": "X"}
# Define when a draw occurs
draw_conditions = {"A": "X" ,"B": "Y" ,"C": "Z"}
# Define when a lose occurs
lose_conditions = {"A": "Z", "B": "X", "C": "Y"}
# Define scores for hand gestures by player and for the game ending
score_map = {"X": 1, "Y": 2, "Z": 3, "LOSE": 0, "WIN": 6, "DRAW": 3}

def is_win(enemy, player): return win_conditions[enemy] == player
def is_draw(enemy, player): return draw_conditions[enemy] == player
def is_lose(enemy, player): return lose_conditions[enemy] == player

def change_player_based_on(enemy, player):
    return win_conditions[enemy] if player == "Z" \
        else lose_conditions[enemy] if player == "X" \
        else draw_conditions[enemy] if player == "Y" \
        else player
  
def solve(puzzle_input, part=1):
    rounds = puzzle_input.split('\n')
    points_per_game = defaultdict(int)
    with tqdm(total=len(rounds)) as pbar:
        for i, round in enumerate(rounds):
            enemy, player = round.split(' ')
            # Change player based on rules for part 2
            if part == 2:
                player = change_player_based_on(enemy, player)
            # Calculate base points for the game
            points_per_game[i] += score_map[player]
            points_per_game[i] += score_map["WIN"] if is_win(enemy, player) \
                                else score_map["DRAW"] if is_draw(enemy, player) \
                                else score_map["LOSE"] if is_lose(enemy, player) \
                                else 0
            pbar.update(1)
    print(f"Points over {len(points_per_game.keys())} games: {sum(points_per_game.values())}")
    
if __name__ == '__main__':
    start_time = time.time()
    solve(read_file(f"python_scripts/day_2.txt"))
    solve(read_file(f"python_scripts/day_2.txt"), part=2)
    print(f"Time elapsed: {time.time() - start_time} seconds")
