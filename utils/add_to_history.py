import os
import json

def add_to_history(total_expression, current_expression):

    script_dir = os.path.dirname(__file__)

    history_path = os.path.join(script_dir, "..", "history", "history.json")

    with open(history_path, "r") as file:
        data = json.load(file)

    data[total_expression] = current_expression

    with open(history_path, "w") as file:
        json.dump(data, file)
