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

    def rotate(self):
        """
        旋转方块
        """
        self.shape = rotate(self.shape)

    def get_rotated(self):
        """
        获取旋转后的形状
        :return: 旋转后的形状
        """
        return rotate(self.shape)

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
        self.level = self.config.get("level", 1)
        self.seven_bag = SevenBag()
        self.current = self._new_tetromino()
        self.next_count = self.config.get("next_count", 6)
        self.next_list = [self._new_tetromino() for _ in range(self.next_count)]
        self.hold = None
        self.hold_used = False
        self.last_drop = time.time()
        self.game_over = False

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
        获取当前下落间隔
        :return: 间隔秒数
        """
        if self.level >= LEVEL_MAX:
            return DROP_TIME_MIN
        t = DROP_TIME_BASE - (self.level - 1) * DROP_TIME_STEP
        return max(DROP_TIME_MIN, t)

    def try_level_up(self):
        """
        检查升级
        """
        new_level = self.score // LEVEL_UP_SCORE + 1
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

        # Hold区（分数和等级下方，Next区上方）
        hold_y = info_y + 3
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
            "  ←/→  左右移动",
            "  ↑    旋转",
            "  ↓    快速下落",
            "  空格  硬降到底",
            "  C    Hold/切换方块",
            "  ESC  暂停并显示本帮助",
            "",
            "按 ESC 或 空格 继续游戏"
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
            if key in (27, ord(' ')):
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
                # ...（省略）...
                while True:
                    if self.stdscr.getch() == ord("q"):
                        return
                    time.sleep(0.1)

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
            elif key == curses.KEY_UP:
                rotated = self.current.get_rotated()
                new_y, new_x = self.wall_kick(self.current, rotated)
                if new_y is not None:
                    self.current.shape = rotated
                    self.current.y = new_y
                    self.current.x = new_x
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
                            elif wait_key == curses.KEY_UP:
                                rotated = self.current.get_rotated()
                                new_y, new_x = self.wall_kick(self.current, rotated, allow_up=True)
                                if new_y is not None:
                                    self.current.shape = rotated
                                    self.current.y = new_y
                                    self.current.x = new_x
                                    touch_time = time.time()
                            elif wait_key == ord(" "):
                                # 空格：硬降到底并立即固定
                                while not self.board.check_collision(self.current, y=self.current.y + 1, x=self.current.x):
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
                        self.board.fix_tetromino(self.current)
                        lines = self.board.remove_full_lines()
                        if lines > 0:
                            self.score += SCORES.get(lines, lines * 100)
                            self.try_level_up()
                        self.current = self.next_list.pop(0)
                        self.next_list.append(self._new_tetromino())
                        self.hold_used = False
                        # 顶部4行有方块则Game Over
                        if self.board.check_collision(self.current):
                            self.game_over = True
                        self.last_drop = time.time()
                        continue
                self.last_drop = time.time()
            time.sleep(0.02)
