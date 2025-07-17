"""
全局常量配置
"""

BOARD_HEIGHT = 24
BOARD_WIDTH = 12
DROP_TIME_BASE = 0.5
DROP_TIME_STEP = 0.05
DROP_TIME_MIN = 0.05
LEVEL_UP_SCORE = 1000
LEVEL_MAX = 18
LEVEL_INIT = 1
SHAPE_CHAR = "■"
GHOST_CHAR = "⧄"
EMPTY_CHAR = "  "
BORDER_TOP_LEFT = "┌"
BORDER_TOP_RIGHT = "┐"
BORDER_BOTTOM_LEFT = "└"
BORDER_BOTTOM_RIGHT = "┘"
BORDER_HORIZONTAL = "─"
BORDER_VERTICAL = "│"
NEXT_COUNT = 4

SCORES = {1: 100, 2: 300, 3: 700, 4: 1500}

TETROMINOS = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
]
