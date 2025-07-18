"""
全局常量配置
"""

BOARD_HEIGHT = 20
BOARD_WIDTH = 10

# 下落速度配置（单位：秒）
DROP_TIME_BASE = 0.8  # 初始下落间隔（比原版略慢，适合新手）
DROP_TIME_MIN = 0.03  # 最小下落间隔（极限速度更快）

# 等级配置
LEVEL_INIT = 1  # 初始等级
LEVEL_MAX = 15  # 最大等级（降低总等级数，但更具挑战性）
LEVEL_UP_BASE = 500  # 基础升级分数
LEVEL_UP_FACTOR = 1.5  # 升级分数增长因子（指数增长）

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

TETROMINOS = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
]
