from collections import defaultdict
import time
from tqdm import tqdm
import os
import pickle
import pandas as pd
from sklearn.tree import DecisionTreeRegressor

GBR = None

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

def create_train_model():
    if not os.path.exists("python_scripts/day_2_model.pkl"):
        # train a gradient boosting regressor on the data
        df = pd.read_csv("python_scripts/day_2_data.csv")
        X = df.drop("score", axis=1)
        y = df["score"]
        gbr = DecisionTreeRegressor()
        gbr.fit(X, y)
        # with open("day_2_model.pkl", "wb") as f:
        #     pickle.dump(gbr, f)
        return gbr
    else:
        with open("python_scripts/day_2_model.pkl", "rb") as f:
            return pickle.load(f)
  
def predict_score(player, enemy):
    global GBR
    data = {"player_X": 0, "player_Y": 0, "player_Z": 0, "enemy_A": 0, "enemy_B": 0, "enemy_C": 0}
    data[f"player_{player}"] = 1
    data[f"enemy_{enemy}"] = 1
    # pd from records
    data = pd.DataFrame.from_records([data])
    return GBR.predict(data)[0]

def solve(puzzle_input):
    global GBR
    rounds = puzzle_input.split('\n')
    points_per_game = defaultdict(int)
    GBR = create_train_model()
    with tqdm(total=len(rounds)) as pbar:
        for i, round in enumerate(rounds):
            enemy, player = round.split(' ')
            points_per_game[i] += predict_score(player, enemy)
            pbar.set_postfix_str(f"Current Points: {sum(points_per_game.values())}")
            pbar.update(1)
    print(f"Points over {len(points_per_game.keys())} games: {int(sum(points_per_game.values()))}")

if __name__ == '__main__':
    start_time = time.time()
    solve(read_file("python_scripts/day_2.txt"))
    print(f"Time elapsed: {time.time() - start_time} seconds")