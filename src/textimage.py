import subprocess
from pathlib import Path

from PIL import Image, ImageFont, ImageDraw

COLORS = {
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "ping": (255, 192, 203),
    "orange": (255, 165, 0),
    "yellow": (255, 255, 0),
    "purple": (128, 0, 128),
    "green": (0, 128, 0),
    "blue": (0, 0, 255),
    "brown": (165, 42, 42),
    "white": (255, 255, 255),
    "grey": (128, 128, 128),
    "transparent": (0, 0, 0, 0),
}


def parse_color(text):
    # Color codes from https://htmlcolorcodes.com/color-names/
    if text.lower() in COLORS:
        return (
            COLORS[text.lower()] + (255,)
            if len(COLORS[text.lower()]) == 3
            else COLORS[text.lower()]
        )

    try:
        result = tuple(
            [
                int(x)
                for x in text.replace(" ", "")
                .replace("(", "")
                .replace(")", "")
                .split(",")
            ][:4]
        )
        if len(result) != 4:
            raise ValueError("invalid color value")
        return result
    except ValueError:
        raise ValueError("invalid color value")


class Text:
    def __init__(self):
        self.content = None
        self.font_name = "sans-serif"
        self.color = (0, 0, 0, 255)

    def set_color(self, text):
        self.color = parse_color(text)

    def resolve_font(self, size):
        try:
            return ImageFont.truetype(self.font_name, size)
        except OSError:
            try:
                self.font_name = (
                    subprocess.check_output(["fc-match", self.font_name])
                    .decode()
                    .partition(":")[0]
                )
                return ImageFont.truetype(self.font_name, size)
            except (FileNotFoundError, OSError):
                return None


class TextImage:

    def __init__(self):
        self.text_list = []
        self.size = (0, 0)
        self.text_size = 500
        self.line_spacing = 3 / 2
        self.padding = 1
        self.background_color = (255, 255, 255, 255)
        self.image = None
        self.save_path = None

    def generate_image(self):
        self.image = Image.new("RGBA", self.size, self.background_color)
        draw = ImageDraw.Draw(self.image)

        max_length = 0
        spacing = self.text_size * 2 / 3
        length = spacing * self.padding
        height = spacing / 2 + spacing * self.padding
        last_text = ""
        for text_index, text_element in enumerate(self.text_list):
            text_element.resolve_font(self.text_size)
            font = text_element.resolve_font(self.text_size)
            for line_index, line in enumerate(text_element.content.split("\n")):
                if line == "":
                    continue
                if line_index > 0:
                    height += spacing * self.line_spacing
                    length = spacing * self.padding
                    last_text = ""
                length += draw.textlength(last_text + line, font=font) / 2
                max_length = max(
                    length + draw.textlength(line, font=font) / 2, max_length
                )
                draw.text(
                    (length, height),
                    line,
                    font=font,
                    fill=text_element.color,
                    anchor="mm",
                )
                last_text = line
        height += spacing / 2 + spacing * self.padding
        max_length += spacing * self.padding
        if self.size == (0, 0):
            self.size = (int(max_length), int(height))
            return self.generate_image()

    def add_custom_text(self, text):
        self.text_list.append(text)

    def set_color(self, text):
        self.background_color = parse_color(text)

    def preview_image(self):
        if self.image:
            self.image.show()

    def save_image(self):
        if Path(self.save_path).is_file():
            raise FileExistsError("target save path already exists")
        self.image.save(self.save_path)
