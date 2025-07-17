# tetris

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tetris.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

俄罗斯方块命令行游戏，基于 Python [curses](https://docs.python.org/3/library/curses.html) 和 [Typer](https://typer.tiangolo.com/) 实现，支持多种参数自定义，支持预告方块、影子方块、难度调节等特性。

## 特性

- 纯命令行界面，跨平台（Linux/macOS，Windows 需支持 curses）
- 支持自定义棋盘大小、下落速度、难度、方块字符等
- 支持影子方块（落点预览）
- 支持多预告方块
- 支持暂停、加速、硬降
- 支持 Hold/切换方块
- 代码结构清晰，易于扩展
- 单元测试覆盖核心逻辑

## 安装

推荐使用 Python 3.7 及以上版本。

```bash
git clone https://github.com/lonsty/tetris.git
cd tetris
pip install .
```

或直接通过 pip 安装：

```bash
pip install tetris
```

## 快速开始

在终端输入：

```bash
tetris
```

即可开始游戏。

## 操作说明

- **←**：左移
- **→**：右移
- **↓**：加速下落（只加速，不会固定方块）
- **↑**：旋转
- **空格**：硬降（直接落到底并固定）
- **C**：Hold/切换方块（每个方块只可 Hold 一次）
- **ESC**：暂停并显示帮助
- **q**：退出游戏

## 命令行参数

所有参数均有默认值，可通过命令行自定义。例如：

```bash
tetris --board-height 24 --board-width 12 --next-count 2 --shape-char "□"
```

### 支持的参数

| 参数名                | 默认值 | 说明                       |
|-----------------------|--------|----------------------------|
| --board-height        | 20     | 棋盘高度                   |
| --board-width         | 10     | 棋盘宽度                   |
| --drop-time-base      | 0.5    | 初始下落间隔（秒）         |
| --drop-time-step      | 0.05   | 每升一级减少的间隔（秒）   |
| --drop-time-min       | 0.05   | 最快下落间隔（秒）         |
| --level-up-score      | 1000   | 每升一级所需分数           |
| --level-max           | 18     | 最高难度等级               |
| --shape-char          | "■"    | 方块字符                   |
| --ghost-char          | "⧄"    | 影子字符                   |
| --empty-char          | "  "   | 空白字符                   |
| --border-top-left     | "┌"    | 左上角边框                 |
| --border-top-right    | "┐"    | 右上角边框                 |
| --border-bottom-left  | "└"    | 左下角边框                 |
| --border-bottom-right | "┘"    | 右下角边框                 |
| --border-horizontal   | "─"    | 水平边框                   |
| --border-vertical     | "│"    | 垂直边框                   |
| --next-count          | 4      | 预告方块数量（1~6）        |

查看所有参数及帮助：

```bash
tetris --help
```

## 运行效果

![tetris-demo]()

## 开发与测试

1. 克隆仓库并安装依赖：

    ```bash
    git clone https://github.com/lonsty/tetris.git
    cd tetris
    pip install -e .[dev]
    ```

2. 运行单元测试：

    ```bash
    python -m unittest discover tests
    ```

3. 代码结构：

    ```
    tetris/
      ├── __init__.py
      ├── cli.py         # Typer 命令行入口
      ├── tetris.py      # 游戏主逻辑
      ├── const.py       # 常量配置
      └── utils.py       # 工具函数
    tests/               # 单元测试
    ```

## 贡献

欢迎提交 issue 和 PR！

- 发现 bug 或有新建议，请在 [Issues](https://github.com/lonsty/tetris/issues) 区留言。
- 代码贡献请遵循 [PEP8](https://www.python.org/dev/peps/pep-0008/) 风格。

## 许可证

MIT License © 2025 [Allen Shaw](mailto:lonsty@sina.com)

详见 [LICENSE](LICENSE)

---

**项目主页**：[https://github.com/lonsty/tetris](https://github.com/lonsty/tetris)
