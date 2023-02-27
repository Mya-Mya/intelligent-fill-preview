from dataclasses import dataclass


@dataclass
class Color:
    """
    Represents a color data.
    """
    r: int
    g: int
    b: int


def convert_color_to_hexcolor(color: Color)->str:
    """
    Converts from Color dataclass to str in hex format.
    """
    return "#{:02x}{:02x}{:02x}".format(color.r, color.g, color.b)
