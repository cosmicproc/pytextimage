import platform

import textimage

if platform.system() == "Windows":
    import os

    # Fix ANSI escape codes on Windows
    os.system("")

COLORS_CODES = {
    "BLACK": "\033[30m",
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[33m",
    "BLUE": "\033[34m",
    "PURPLE": "\033[35m",
    "CYAN": "\033[36m",
    "WHITE": "\033[37m",
    "RESET": "\033[0m",
}


def colorify(func):
    def new_func(*args, color=None, **kwargs):
        if color:
            print(COLORS_CODES[color], end="")
        func(*args, **kwargs)
        if color:
            print(COLORS_CODES["RESET"], end="")

    return new_func


colored_print = colorify(print)


def ask_text():
    text = textimage.Text()
    text.content = input("Enter a text piece: ").replace("\\n", "\n")
    while len(text.content) < 1:
        colored_print("Text piece cannot be empty.", color="RED")
        text.content = input("Enter a text piece: ").replace("\\n", "\n")
    text_font = input("Enter the text font (default = '" + text.font_name + "'): ")
    if text_font:
        text.font_name = text_font
    while True:
        try:
            text_color = input(
                "Enter the text color (default = '" + str(text.color) + "'): "
            )
            if text_color:
                text.set_color(text_color)
            break
        except ValueError:
            colored_print("Invalid color value.", color="RED")
            print("Enter the color in the RGBA format. (example: '255, 0, 0, 255')")
    return text


def interact(design):
    while True:
        text_size = input(
            "Enter the text size (default = '" + str(design.text_size) + "'): "
        )
        try:
            if text_size:
                design.text_size = int(text_size)
            break
        except ValueError:
            colored_print("Invalid size value. (must be an integer)", color="RED")
    while True:
        background_color = input(
            "Enter the background color of the image (default = '"
            + str(design.background_color)
            + "'): "
        )
        try:
            if background_color:
                design.set_color(background_color)
            break
        except ValueError:
            colored_print("Invalid color value.", color="RED")
            print("Enter the color in the RGBA format. (example: '255, 0, 0, 255')")
    while True:
        design.add_custom_text(ask_text())
        prompt = input("Do you want to add another text piece [y/N]: ")
        if prompt.lower() != "y" and prompt.lower() != "yes":
            break
    design.generate_image()
    prompt = input("Do you want to preview the image [Y/n]: ")
    if prompt.lower() != "n" and prompt.lower() != "no":
        design.preview_image()
        while True:
            design.save_path = input(
                "Enter the save path for the image (leave empty to not save): "
            )
            try:
                if design.save_path:
                    design.save_image()
                break
            except OSError:
                colored_print("Invalid save path.", color="RED")
                print("Note: Only PNG file format is supported.")
