#!/usr/bin/env python3

import os
import json

def clear_history():
    script_dir = os.path.dirname(__file__)

    history_path = os.path.join(script_dir, "..", "history", "history.json")

    with open(history_path, "w") as file:
        json.dump({}, file)
