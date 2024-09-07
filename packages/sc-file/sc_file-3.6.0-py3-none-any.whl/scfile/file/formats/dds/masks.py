from typing import TypeAlias


Mask: TypeAlias = tuple[int, int, int, int]

RGBA8 = (0xFF, 0xFF00, 0xFF0000, 0xFF)
BGRA8 = (0xFF0000, 0xFF00, 0xFF, 0xFF)
