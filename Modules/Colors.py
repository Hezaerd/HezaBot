from random import randint


class Embed:
    """Color class (embed purpose)"""
    Red = Error = 0xff0000
    Green = Success = 0x00ff00
    Blue = Info = 0x00ffff
    Yellow = Warning = 0xffff00
    Purple = 0x800080
    Pink = 0xffc0cb
    Black = 0x000000
    White = 0xffffff
    Gray = 0x808080
    Orange = 0xffa500
    Gold = Similar = 0xe09026

    @staticmethod
    def color_from_rgb(r: int, g: int, b: int) -> int:
        """Convert RGB to hex"""
        return (r << 16) + (g << 8) + b

    @staticmethod
    def random() -> int:
        """Generate a random color"""
        return randint(0, 0xffffff)