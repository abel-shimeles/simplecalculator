#!/usr/bin/env python3

import os
import json


def get_settings():
    script_dir = os.path.dirname(__file__)

    settings_path = os.path.join(script_dir, "..", "settings", "settings.json")

    with open(settings_path, "r") as file:
        data = json.load(file)

        settings = {
            "large_font_style": tuple(data["fonts"]["LARGE_FONT_STYLE"]),
            "small_font_style": tuple(data["fonts"]["SMALL_FONT_STYLE"]),
            "digits_font_style": tuple(data["fonts"]["DIGITS_FONT_STYLE"]),
            "default_font_style": tuple(data["fonts"]["DEFAULT_FONT_STYLE"]),
            "operators_font_style": tuple(data["fonts"]["OPERATORS_FONT_STYLE"]),
            "special_characters_color": data["colors"]["SPECIAL_CHARACTERS"],
            "digits_color": data["colors"]["DIGITS"],
            "equals_color": data["colors"]["EQUALS"],
            "display_labels_color": data["colors"]["DISPLAY_LABELS"],
            "label_color": data["colors"]["LABEL_COLOR"],
            "clear_color": data["colors"]["CLEAR_COLOR"],
        }

        return settings
