def rotate(shape):
    """
    旋转方块
    :param shape: 方块二维数组
    :return: 旋转后的方块
    """
    return [list(row) for row in zip(*shape[::-1])]


def deep_copy_shape(shape):
    """
    深拷贝方块
    :param shape: 方块二维数组
    :return: 拷贝后的方块
    """
    return [row[:] for row in shape]
