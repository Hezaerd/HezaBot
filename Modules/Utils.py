from random import randint


def color_from_rgb(r: int, g: int, b: int) -> int:
    """Convert RGB to hex"""
    return (r << 16) + (g << 8) + b


def color_random() -> int:
    """Generate a random color"""
    return randint(0, 0xffffff)