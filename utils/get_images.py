#!/usr/bin/env python3

import os

def get_images():

    script_dir = os.path.dirname(__file__)

    images = {
        "favicon_path": os.path.join(script_dir, "..", "images", "favicon.png"),
        "history_icon_path": os.path.join(
            script_dir, "..", "images", "history_icon.png"
        ),
        "clear_history_path": os.path.join(
            script_dir, "..", "images", "clear_history_icon.png"
        ),
    }

    return images
