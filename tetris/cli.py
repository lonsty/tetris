# tetris/cli.py
import curses

import typer

from tetris.const import *
from tetris.tetris import TetrisGame

app = typer.Typer(help="俄罗斯方块命令行游戏")


def run_game(
    board_height: int,
    board_width: int,
    drop_time_base: float,
    drop_time_min: float,
    level_max: int,
    level: int,
    shape_char: str,
    ghost_char: str,
    empty_char: str,
    border_top_left: str,
    border_top_right: str,
    border_bottom_left: str,
    border_bottom_right: str,
    border_horizontal: str,
    border_vertical: str,
    next_count: int,
):
    config = {
        "board_height": board_height,
        "board_width": board_width,
        "drop_time_base": drop_time_base,
        "drop_time_min": drop_time_min,
        "level_max": level_max,
        "level": level,
        "shape_char": shape_char,
        "ghost_char": ghost_char,
        "empty_char": empty_char,
        "border_top_left": border_top_left,
        "border_top_right": border_top_right,
        "border_bottom_left": border_bottom_left,
        "border_bottom_right": border_bottom_right,
        "border_horizontal": border_horizontal,
        "border_vertical": border_vertical,
        "next_count": next_count,
    }

    def _main(stdscr):
        game = TetrisGame(stdscr, config)
        game.run()

    curses.wrapper(_main)


@app.callback(invoke_without_command=True)
def main(
    board_height: int = typer.Option(BOARD_HEIGHT, help="棋盘高度"),
    board_width: int = typer.Option(BOARD_WIDTH, help="棋盘宽度"),
    drop_time_base: float = typer.Option(DROP_TIME_BASE, help="初始下落间隔（秒）"),
    drop_time_min: float = typer.Option(DROP_TIME_MIN, help="最快下落间隔（秒）"),
    level_max: int = typer.Option(LEVEL_MAX, help="最高难度等级"),
    level: int = typer.Option(LEVEL_INIT, help="初始等级"),
    shape_char: str = typer.Option(SHAPE_CHAR, help="方块字符"),
    ghost_char: str = typer.Option(GHOST_CHAR, help="影子字符"),
    empty_char: str = typer.Option(EMPTY_CHAR, help="空白字符"),
    border_top_left: str = typer.Option(BORDER_TOP_LEFT, help="左上角边框"),
    border_top_right: str = typer.Option(BORDER_TOP_RIGHT, help="右上角边框"),
    border_bottom_left: str = typer.Option(BORDER_BOTTOM_LEFT, help="左下角边框"),
    border_bottom_right: str = typer.Option(BORDER_BOTTOM_RIGHT, help="右下角边框"),
    border_horizontal: str = typer.Option(BORDER_HORIZONTAL, help="水平边框"),
    border_vertical: str = typer.Option(BORDER_VERTICAL, help="垂直边框"),
    next_count: int = typer.Option(NEXT_COUNT, help="预告方块数量"),
):
    """
    直接运行 tetris 即可启动游戏。
    """
    run_game(
        board_height,
        board_width,
        drop_time_base,
        drop_time_min,
        level_max,
        level,
        shape_char,
        ghost_char,
        empty_char,
        border_top_left,
        border_top_right,
        border_bottom_left,
        border_bottom_right,
        border_horizontal,
        border_vertical,
        next_count,
    )


def run():
    app()
