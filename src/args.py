import argparse
import importlib.metadata

import textimage

__version__ = importlib.metadata.version("pytextimage")

HELP_INFO = {
    "text": "add text to your image (content, font, color) (example: 'pytextimage sans-serif red')",
    "size": "size of the image",
    "background_color": "color for your image background in RGBA format (example: '255, 0, 0, 255')",
    "save_path": "path to save your generated image",
    "text_size": "size of the text in the image",
    "line_spacing": "scale of the size of the spaces between lines (default is 3/2)",
    "padding": "scale of the size of padding of the image",
}


def set_parser():
    parser = argparse.ArgumentParser(
        prog="pytextimage", description="Generate custom images with text easily."
    )

    parser.add_argument(
        "-v", "--version", action="version", version="pytextimage " + __version__
    )
    parser.add_argument(
        "-t",
        "--text",
        type=str,
        nargs="+",
        action="append",
        dest="text",
        help=HELP_INFO["text"],
    )
    parser.add_argument(
        "-b",
        "--background_color",
        type=str,
        dest="background_color",
        help=HELP_INFO["background_color"],
    )
    parser.add_argument(
        "-T", "--text_size", type=int, dest="text_size", help=HELP_INFO["text_size"]
    )
    parser.add_argument(
        "-l",
        "--line_spacing",
        type=float,
        dest="line_spacing",
        help=HELP_INFO["line_spacing"],
    )
    parser.add_argument(
        "-p", "--padding", type=float, dest="padding", help=HELP_INFO["padding"]
    )
    parser.add_argument(
        "-s", "--save", type=str, dest="save_path", help=HELP_INFO["save_path"]
    )
    return parser


def configure_with_args(design):
    parser = set_parser()
    args = parser.parse_args()
    if args.background_color:
        design.set_color(args.background_color)
    if args.save_path:
        design.save_path = args.save_path
    if args.text_size is not None:
        design.text_size = args.text_size
    if args.line_spacing is not None:
        design.line_spacing = args.line_spacing
    if args.padding is not None:
        design.padding = args.padding
    if not args.text:
        return None
    for arg in args.text:
        new_text = textimage.Text()
        new_text.content = arg[0].replace("\\n", "\n")
        if len(arg) > 4:
            parser.error("argument -t/--text cannot take more than 2 values")
        if len(arg) >= 2 and arg[1] != "-":
            new_text.font_name = arg[1]
        if len(arg) == 3 and arg[2] != "-":
            new_text.set_color(arg[2])
        design.add_custom_text(new_text)
    return design
