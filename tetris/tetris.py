import curses
import random
import time

from tetris.const import *
from tetris.utils import deep_copy_shape, rotate


class Tetromino:
    """
    方块类
    """

    def __init__(self, shape, y, x):
        """
        :param shape: 方块形状（二维列表）
        :param y: 初始y坐标
        :param x: 初始x坐标
        """
        self.shape = deep_copy_shape(shape)
        self.y = y
        self.x = x
        # 记录旋转方向（0: 未旋转, 1: 顺时针, -1: 逆时针）
        self.rotation_direction = 0

    def get_coords(self, y=None, x=None, shape=None):
        """
        获取方块所有格子的坐标
        :param y: y坐标（可选，默认当前y）
        :param x: x坐标（可选，默认当前x）
        :param shape: 形状（可选，默认当前形状）
        :return: 坐标列表
        """
        if y is None:
            y = self.y
        if x is None:
            x = self.x
        if shape is None:
            shape = self.shape
        coords = []
        for dy, row in enumerate(shape):
            for dx, cell in enumerate(row):
                if cell:
                    coords.append((y + dy, x + dx))
        return coords

    def rotate_clockwise(self):
        """
        顺时针旋转方块
        """
        self.shape = rotate(self.shape)
        self.rotation_direction = 1

    def rotate_counterclockwise(self):
        """
        逆时针旋转方块
        """
        # 逆时针旋转相当于顺时针旋转3次
        for _ in range(3):
            self.shape = rotate(self.shape)
        self.rotation_direction = -1

    def get_rotated_clockwise(self):
        """
        获取顺时针旋转后的形状
        :return: 旋转后的形状
        """
        return rotate(self.shape)

    def get_rotated_counterclockwise(self):
        """
        获取逆时针旋转后的形状
        :return: 旋转后的形状
        """
        shape = self.shape
        for _ in range(3):
            shape = rotate(shape)
        return shape

    def width(self):
        """
        :return: 方块宽度
        """
        return len(self.shape[0])

    def height(self):
        """
        :return: 方块高度
        """
        return len(self.shape)

    def is_I(self):
        """
        是否为I型方块
        :return: bool
        """
        return (
            self.shape == TETROMINOS[0]
            or self.shape == rotate(TETROMINOS[0])
            or self.shape == rotate(rotate(TETROMINOS[0]))
            or self.shape == rotate(rotate(rotate(TETROMINOS[0])))
        )

    def is_T(self):
        """
        是否为T型方块
        :return: bool
        """
        # T型方块原始形状
        original_T = TETROMINOS[2]
        # 检查当前形状是否是T型方块的旋转变体
        return (
            self.shape == original_T
            or self.shape == rotate(original_T)
            or self.shape == rotate(rotate(original_T))
            or self.shape == rotate(rotate(rotate(original_T)))
        )


class SevenBag:
    """
    7-bag 随机系统
    """

    def __init__(self):
        """
        :param: 无
        """
        self.bag = []

    def next(self):
        """
        获取下一个方块形状
        :return: 形状（二维列表）
        """
        if not self.bag:
            self.bag = list(TETROMINOS)
            random.shuffle(self.bag)
        return self.bag.pop()


class Board:
    """
    游戏棋盘
    """

    def __init__(self, height, width):
        """
        :param height: 棋盘高度（含隐藏区）
        :param width: 棋盘宽度
        """
        self.height = height
        self.width = width
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

    def check_collision(self, tetromino, y=None, x=None, shape=None):
        """
        检查方块是否碰撞
        :param tetromino: 方块对象
        :param y: y坐标
        :param x: x坐标
        :param shape: 形状
        :return: 是否碰撞
        """
        if y is None:
            y = tetromino.y
        if x is None:
            x = tetromino.x
        if shape is None:
            shape = tetromino.shape
        for dy, row in enumerate(shape):
            for dx, cell in enumerate(row):
                if cell:
                    by, bx = y + dy, x + dx
                    if by < 0 or by >= self.height or bx < 0 or bx >= self.width or self.grid[by][bx]:
                        return True
        return False

    def fix_tetromino(self, tetromino):
        """
        固定方块到棋盘
        :param tetromino: 方块对象
        """
        for y, x in tetromino.get_coords():
            if 0 <= y < self.height and 0 <= x < self.width:
                self.grid[y][x] = 1

    def remove_full_lines(self):
        """
        消除满行
        :return: 消除的行数
        """
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        lines_cleared = self.height - len(new_grid)
        while len(new_grid) < self.height:
            new_grid.insert(0, [0 for _ in range(self.width)])
        self.grid = new_grid
        return lines_cleared

    def is_perfect_clear(self):
        """
        检查是否完美清除（整个棋盘为空）
        :return: bool
        """
        for row in self.grid:
            if any(cell != 0 for cell in row):
                return False
        return True

    def draw(self, stdscr, offset_y=0, offset_x=0):
        """
        绘制棋盘（只显示底部20行）
        :param stdscr: curses窗口
        :param offset_y: y偏移
        :param offset_x: x偏移
        """
        # 上边框
        stdscr.addstr(offset_y, offset_x, BORDER_TOP_LEFT + BORDER_HORIZONTAL * (self.width * 2 - 1) + BORDER_TOP_RIGHT)
        # 内容和左右边框
        for y in range(4, self.height):  # 只显示底部20行
            stdscr.addstr(offset_y + 1 + (y - 4), offset_x, BORDER_VERTICAL)
            for x in range(self.width):
                if self.grid[y][x]:
                    stdscr.addstr(offset_y + 1 + (y - 4), offset_x + 1 + x * 2, SHAPE_CHAR)
                else:
                    stdscr.addstr(offset_y + 1 + (y - 4), offset_x + 1 + x * 2, EMPTY_CHAR)
            stdscr.addstr(offset_y + 1 + (y - 4), offset_x + 1 + (self.width * 2 - 1), BORDER_VERTICAL)
        # 下边框
        stdscr.addstr(
            offset_y + 1 + (self.height - 4),
            offset_x,
            BORDER_BOTTOM_LEFT + BORDER_HORIZONTAL * (self.width * 2 - 1) + BORDER_BOTTOM_RIGHT,
        )

    def draw_tetromino(self, stdscr, tetromino, char, offset_y=0, offset_x=0):
        """
        绘制活动方块
        :param stdscr: curses窗口
        :param tetromino: 方块对象
        :param char: 显示字符
        :param offset_y: y偏移
        :param offset_x: x偏移
        """
        for y, x in tetromino.get_coords():
            if 4 <= y < self.height and 0 <= x < self.width:
                stdscr.addstr(offset_y + 1 + (y - 4), offset_x + 1 + x * 2, char)

    def get_ghost_y(self, tetromino):
        """
        获取影子方块的y坐标
        :param tetromino: 方块对象
        :return: y坐标
        """
        ghost_y = tetromino.y
        while not self.check_collision(tetromino, y=ghost_y + 1, x=tetromino.x):
            ghost_y += 1
        return ghost_y

    def check_t_spin(self, tetromino):
        """
        检查是否为T-Spin
        :param tetromino: T型方块对象
        :return: 是否为T-Spin
        """
        if not tetromino.is_T():
            return False

        # 获取T方块中心坐标
        center_y = tetromino.y + len(tetromino.shape) // 2
        center_x = tetromino.x + len(tetromino.shape[0]) // 2

        # 定义四个角落坐标
        corners = [
            (center_y - 1, center_x - 1),  # 左上
            (center_y - 1, center_x + 1),  # 右上
            (center_y + 1, center_x - 1),  # 左下
            (center_y + 1, center_x + 1),  # 右下
        ]

        # 计算被占据的角落数量
        occupied_corners = 0
        for y, x in corners:
            if y < 0 or y >= self.height or x < 0 or x >= self.width:
                occupied_corners += 1  # 边界视为被占据
            elif self.grid[y][x]:
                occupied_corners += 1

        # T-Spin需要至少三个角落被占据
        return occupied_corners >= 3


class TetrisGame:
    """
    俄罗斯方块游戏主类
    """

    def __init__(self, stdscr, config=None):
        """
        :param stdscr: curses窗口
        :param config: 配置字典
        """
        self.stdscr = stdscr
        self.config = config or {}
        self.board = Board(24, 10)  # 24行10列，含4行隐藏区
        self.score = 0
        self.level = self.config.get("level", LEVEL_INIT)
        self.level_thresholds = self._precompute_level_thresholds()
        self.seven_bag = SevenBag()
        self.current = self._new_tetromino()
        self.next_count = self.config.get("next_count", 6)
        self.next_list = [self._new_tetromino() for _ in range(self.next_count)]
        self.hold = None
        self.hold_used = False
        self.last_drop = time.time()
        self.game_over = False
        # 记录上一次消除类型（用于Back-to-Back判断）
        self.last_clear_type = None  # None, 'normal', 't-spin'
        # 连击计数器
        self.combo_count = 0
        # 记录当前方块是否被旋转过（用于T-Spin检测）
        self.current_rotated = False

    def _precompute_level_thresholds(self):
        """预计算所有等级升级所需的分数门槛"""
        thresholds = [0]  # 等级1的门槛为0
        for level in range(2, LEVEL_MAX + 2):  # 计算到LEVEL_MAX+1级
            exponent = level - 2  # 指数计算
            threshold = LEVEL_UP_BASE * (LEVEL_UP_FACTOR**exponent)
            thresholds.append(round(threshold))  # 四舍五入取整
        return thresholds

    def _new_tetromino(self):
        """
        生成新方块（7-bag 随机）
        :return: Tetromino对象
        """
        shape = self.seven_bag.next()
        # 标准起始位置：x=3, y=0
        return Tetromino(shape, 0, 3)

    def wall_kick(self, tetromino, rotated_shape, allow_up=False):
        """
        SRS墙踢/地踢（简化实现）
        :param tetromino: 方块对象
        :param rotated_shape: 旋转后的形状
        :param allow_up: 是否允许向上踢
        :return: (new_y, new_x)
        """
        is_I = (len(rotated_shape) == 1 or len(rotated_shape[0]) == 1) and sum(sum(row) for row in rotated_shape) == 4
        dx_range = [0, -1, 1, -2, 2, -3, 3] if is_I else [0, -1, 1, -2, 2]
        dy_range = [0]
        if allow_up:
            dy_range = [0, -1, -2, -3] if is_I else [0, -1, -2]
        for dy in dy_range:
            for dx in dx_range:
                new_y = tetromino.y + dy
                new_x = tetromino.x + dx
                if not self.board.check_collision(tetromino, y=new_y, x=new_x, shape=rotated_shape):
                    return new_y, new_x
        return None, None

    def get_drop_time(self):
        """
        根据当前等级获取下落时间间隔
        使用分段函数实现非线性速度变化
        """
        if self.level <= 5:
            # 1-5级：每级减少0.12秒
            return DROP_TIME_BASE - (self.level - 1) * 0.12
        elif self.level <= 10:
            # 6-10级：每级减少0.04秒
            return 0.25 - (self.level - 5) * 0.04
        else:
            # 10级以上：每级减少0.005秒，最低不低于DROP_TIME_MIN
            drop_time = 0.07 - (self.level - 10) * 0.005
            return max(drop_time, DROP_TIME_MIN)

    def try_level_up(self):
        """
        检查升级，支持跨级升级
        基于指数增长的门槛分数系统
        """
        # 如果已经是最高等级，不再升级
        if self.level >= LEVEL_MAX:
            return

        # 计算可能达到的最高等级
        new_level = self.level
        for level in range(self.level + 1, LEVEL_MAX + 1):
            # 检查分数是否达到该等级的门槛
            if self.score >= self.level_thresholds[level]:
                new_level = level
            else:
                # 遇到第一个不满足的等级即可停止（门槛分数单调递增）
                break

        # 如果等级有提升
        if new_level > self.level:
            self.level = new_level

    def draw(self):
        """
        绘制游戏界面（局中居中显示，Hold区在分数/等级下方，Next区上方，适配任意next_count）
        :param self: TetrisGame实例
        """
        self.stdscr.clear()
        max_y, max_x = self.stdscr.getmaxyx()
        board_width_px = self.board.width * 2 + 1  # 棋盘宽度（含边框）
        board_height_px = 20 + 2  # 只显示底部20行
        # 计算居中偏移
        offset_y = (max_y - board_height_px) // 2
        offset_x = (max_x - board_width_px) // 2

        # 绘制棋盘
        self.board.draw(self.stdscr, offset_y, offset_x)
        # 影子
        ghost_y = self.board.get_ghost_y(self.current)
        if ghost_y != self.current.y:
            ghost = Tetromino(self.current.shape, ghost_y, self.current.x)
            self.board.draw_tetromino(self.stdscr, ghost, GHOST_CHAR, offset_y, offset_x)
        # 当前方块
        self.board.draw_tetromino(self.stdscr, self.current, SHAPE_CHAR, offset_y, offset_x)

        # 分数、等级和Hold、Next，显示在棋盘右侧
        info_x = offset_x + board_width_px + 4
        info_y = offset_y

        # 分数和等级
        self.stdscr.addstr(info_y, info_x, f"Score: {self.score}")
        self.stdscr.addstr(info_y + 1, info_x, f"Level: {self.level}")
        self.stdscr.addstr(info_y + 2, info_x, f"Combo: {self.combo_count}")

        # Hold区（分数和等级下方，Next区上方）
        hold_y = info_y + 4
        self.stdscr.addstr(hold_y, info_x, "Hold:")
        hold_content_y = hold_y + 1  # Hold内容上方空一行
        # 当前Hold的方块对象
        if self.hold:
            for y, row in enumerate(self.hold.shape):
                for x, cell in enumerate(row):
                    if cell:
                        self.stdscr.addstr(hold_content_y + y, info_x + x * 2, SHAPE_CHAR)
            hold_height = len(self.hold.shape)
        else:
            # Hold为空时，预留4行高度，防止Next区太靠上
            hold_height = 4

        # Next区（Hold区内容下方，自动适配Hold区高度）
        next_y = hold_content_y + hold_height + 1
        self.stdscr.addstr(next_y, info_x, f"Next {self.next_count}:")
        next_content_y = next_y + 1
        # 预览的下一个方块列表
        for idx, tetro in enumerate(self.next_list):
            for y, row in enumerate(tetro.shape):
                for x, cell in enumerate(row):
                    if cell:
                        self.stdscr.addstr(next_content_y + y, info_x + x * 2, SHAPE_CHAR)
            next_content_y += len(tetro.shape) + 1

        # 显示当前状态（T-Spin, Back-to-Back等）
        status_y = next_content_y + 2
        if self.last_clear_type == "t-spin":
            self.stdscr.addstr(status_y, info_x, "T-Spin!")
        elif self.last_clear_type == "back-to-back":
            self.stdscr.addstr(status_y, info_x, "Back-to-Back!")

        self.stdscr.refresh()

    def pause_and_help(self):
        """
        暂停游戏并显示帮助信息，按ESC或空格恢复
        :param self: TetrisGame实例
        """
        self.stdscr.clear()
        max_y, max_x = self.stdscr.getmaxyx()
        help_lines = [
            "游戏已暂停",
            "",
            "操作说明：",
            "  ←/→           左右移动",
            "  ↑/x           顺时针旋转",
            "  z             逆时针旋转",
            "  ↓             快速下落",
            "  空格          硬降到底",
            "  C             Hold/切换方块",
            "  ESC           暂停并显示本帮助",
            "",
            "特殊玩法：",
            "  T-Spin        旋转T型方块到角落",
            "  Back-to-Back  连续T-Spin或消四",
            "  Combo         连续消除行",
            "  Perfect Clear 清空整个棋盘",
            "",
            "按 ESC 或 空格 继续游戏",
        ]
        # 计算最长行长度
        max_line_len = max(len(line) for line in help_lines)
        # 计算整体居中起始x
        block_x = max_x // 2 - max_line_len // 2
        block_y = max_y // 2 - len(help_lines) // 2
        for i, line in enumerate(help_lines):
            self.stdscr.addstr(block_y + i, block_x, line)
        self.stdscr.refresh()
        # 等待ESC或空格
        while True:
            key = self.stdscr.getch()
            if key in (27, ord(" ")):
                break

    def run(self):
        """
        游戏主循环
        """
        curses.curs_set(0)
        self.stdscr.nodelay(1)
        while True:
            self.draw()
            if self.game_over:
                max_y, max_x = self.stdscr.getmaxyx()
                game_over_y = max_y // 2
                game_over_x = max_x // 2 - 5
                self.stdscr.addstr(game_over_y, game_over_x, "游戏结束!")
                self.stdscr.addstr(game_over_y + 1, game_over_x - 5, "按 q 退出, r 重新开始")
                self.stdscr.refresh()
                while True:
                    key = self.stdscr.getch()
                    if key == ord("q"):
                        return
                    elif key == ord("r"):
                        self.__init__(self.stdscr, self.config)
                        break
                    time.sleep(0.1)
                continue

            key = self.stdscr.getch()
            force_fix = False
            # 控制
            if key == ord("q"):
                break
            elif key == curses.KEY_LEFT:
                if not self.board.check_collision(self.current, y=self.current.y, x=self.current.x - 1):
                    self.current.x -= 1
            elif key == curses.KEY_RIGHT:
                if not self.board.check_collision(self.current, y=self.current.y, x=self.current.x + 1):
                    self.current.x += 1
            elif key == curses.KEY_DOWN:
                # 下方向键：只加速下落，不触发固定
                if not self.board.check_collision(self.current, y=self.current.y + 1, x=self.current.x):
                    self.current.y += 1
            elif key == curses.KEY_UP or key == ord("x"):  # 顺时针旋转
                rotated = self.current.get_rotated_clockwise()
                new_y, new_x = self.wall_kick(self.current, rotated)
                if new_y is not None:
                    self.current.shape = rotated
                    self.current.y = new_y
                    self.current.x = new_x
                    self.current_rotated = True
            elif key == ord("z"):  # 逆时针旋转
                rotated = self.current.get_rotated_counterclockwise()
                new_y, new_x = self.wall_kick(self.current, rotated)
                if new_y is not None:
                    self.current.shape = rotated
                    self.current.y = new_y
                    self.current.x = new_x
                    self.current_rotated = True
            elif key == ord(" "):
                # 空格：硬降到底并立即固定
                while not self.board.check_collision(self.current, y=self.current.y + 1, x=self.current.x):
                    self.current.y += 1
                force_fix = True
            elif key == ord("c"):
                # Hold功能
                if not self.hold_used:
                    if self.hold is None:
                        self.hold = Tetromino(deep_copy_shape(self.current.shape), 0, 3)
                        self.current = self.next_list.pop(0)
                        self.next_list.append(self._new_tetromino())
                    else:
                        self.current, self.hold = Tetromino(deep_copy_shape(self.hold.shape), 0, 3), Tetromino(
                            deep_copy_shape(self.current.shape), 0, 3
                        )
                    self.hold_used = True
                    self.current_rotated = False  # 重置旋转状态
            elif key == 27:  # ESC
                self.pause_and_help()

            drop_time = self.get_drop_time()
            if time.time() - self.last_drop > drop_time or force_fix:
                if (
                        not self.board.check_collision(self.current, y=self.current.y + 1, x=self.current.x)
                        and not force_fix
                ):
                    self.current.y += 1
                    self.last_drop = time.time()
                else:
                    if force_fix:
                        fixed = True
                    else:
                        touch_time = time.time()
                        fixed = False
                        while not fixed:
                            self.draw()
                            wait_key = self.stdscr.getch()
                            if wait_key == ord("q"):
                                return
                            elif wait_key == curses.KEY_LEFT:
                                if not self.board.check_collision(self.current, y=self.current.y, x=self.current.x - 1):
                                    self.current.x -= 1
                                    touch_time = time.time()
                            elif wait_key == curses.KEY_RIGHT:
                                if not self.board.check_collision(self.current, y=self.current.y, x=self.current.x + 1):
                                    self.current.x += 1
                                    touch_time = time.time()
                            elif wait_key == curses.KEY_UP or wait_key == ord("x"):
                                rotated = self.current.get_rotated_clockwise()
                                new_y, new_x = self.wall_kick(self.current, rotated, allow_up=True)
                                if new_y is not None:
                                    self.current.shape = rotated
                                    self.current.y = new_y
                                    self.current.x = new_x
                                    self.current_rotated = True
                                    touch_time = time.time()
                            elif wait_key == ord("z"):
                                rotated = self.current.get_rotated_counterclockwise()
                                new_y, new_x = self.wall_kick(self.current, rotated, allow_up=True)
                                if new_y is not None:
                                    self.current.shape = rotated
                                    self.current.y = new_y
                                    self.current.x = new_x
                                    self.current_rotated = True
                                    touch_time = time.time()
                            elif wait_key == ord(" "):
                                # 空格：硬降到底并立即固定
                                while not self.board.check_collision(
                                        self.current, y=self.current.y + 1, x=self.current.x
                                ):
                                    self.current.y += 1
                                fixed = True
                                break
                            # 下方向键不再触发固定
                            if not self.board.check_collision(self.current, y=self.current.y + 1, x=self.current.x):
                                self.current.y += 1
                                break
                            if time.time() - touch_time > 1.0:
                                fixed = True
                                break
                            time.sleep(0.02)
                    if fixed:
                        # 检查是否为T-Spin（只有T型且最后一次有旋转才判定）
                        is_t_spin = False
                        if self.current.is_T() and self.current_rotated:
                            is_t_spin = self.board.check_t_spin(self.current)

                        # 固定方块到棋盘
                        self.board.fix_tetromino(self.current)

                        # 消除行
                        lines = self.board.remove_full_lines()

                        # 检查是否为完美清除
                        is_perfect_clear = self.board.is_perfect_clear()

                        # 计算得分
                        base_score = 0
                        spin_bonus = 0
                        back_to_back_bonus = 0
                        perfect_clear_bonus = 0
                        combo_bonus = 0

                        # 基础行消除得分
                        if lines == 1:
                            base_score = 100 * self.level
                        elif lines == 2:
                            base_score = 300 * self.level
                        elif lines == 3:
                            base_score = 500 * self.level
                        elif lines == 4:
                            base_score = 800 * self.level

                        # T-Spin奖励
                        if is_t_spin:
                            if lines == 0:
                                spin_bonus = 400 * self.level  # T-Spin无消除
                            elif lines == 1:
                                spin_bonus = 800 * self.level  # T-Spin Single
                            elif lines == 2:
                                spin_bonus = 1200 * self.level  # T-Spin Double
                            elif lines == 3:
                                spin_bonus = 1600 * self.level  # T-Spin Triple

                        # Back-to-Back奖励（连续T-Spin消除或Tetris）
                        is_b2b = False
                        if (is_t_spin and lines > 0) or lines == 4:
                            if self.last_clear_type in ["t-spin", "back-to-back", "tetris"]:
                                is_b2b = True
                                back_to_back_bonus = int((base_score + spin_bonus) * 0.5)  # 50%额外奖励

                        # 完美清除奖励
                        if is_perfect_clear:
                            if lines == 1:
                                perfect_clear_bonus = 800 * self.level
                            elif lines == 2:
                                perfect_clear_bonus = 1200 * self.level
                            elif lines == 3:
                                perfect_clear_bonus = 1800 * self.level
                            elif lines == 4:
                                perfect_clear_bonus = 2000 * self.level

                        # 连击奖励（combo）：连续多次消除行
                        if lines > 0:
                            combo_bonus = 50 * self.combo_count * self.level
                            self.combo_count += 1
                        else:
                            self.combo_count = 0

                        # 总得分
                        total_score = base_score + spin_bonus + back_to_back_bonus + perfect_clear_bonus + combo_bonus
                        self.score += total_score

                        # 更新消除类型状态
                        if is_t_spin and lines > 0:
                            if is_b2b:
                                self.last_clear_type = "back-to-back"
                            else:
                                self.last_clear_type = "t-spin"
                        elif lines == 4:
                            if is_b2b:
                                self.last_clear_type = "back-to-back"
                            else:
                                self.last_clear_type = "tetris"
                        elif lines > 0:
                            self.last_clear_type = "normal"
                        else:
                            # 没有消除行，保持上一次的类型（不重置last_clear_type）
                            pass

                        # 升级检查
                        self.try_level_up()

                        # 生成新方块
                        self.current = self.next_list.pop(0)
                        self.next_list.append(self._new_tetromino())
                        self.hold_used = False
                        self.current_rotated = False  # 新方块未旋转

                        # 顶部4行有方块则Game Over
                        if self.board.check_collision(self.current):
                            self.game_over = True
                        self.last_drop = time.time()
                        continue
                self.last_drop = time.time()
            time.sleep(0.02)
