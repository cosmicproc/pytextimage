import sys

import args
import interactive
import textimage

DEBUG = False


def main():
    if not DEBUG:
        sys.tracebacklimit = 0
    try:
        design = args.configure_with_args(textimage.TextImage())
        if not design:
            design = textimage.TextImage()
            interactive.interact(design)
        else:
            design.generate_image()
            if design.save_path:
                design.save_image()
            else:
                design.preview_image()
    except KeyboardInterrupt:
        print("\nQuiting...")


if __name__ == "__main__":
    main()
