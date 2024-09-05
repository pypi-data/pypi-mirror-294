from typing import Tuple, Optional

def move(pos: Tuple[int, int], relative: bool = False) -> None:
    """
    移动鼠标到指定位置。

    参数:
        pos (Tuple[int, int]): 目标坐标，格式为 (x, y)。
        relative (bool): 如果为 True，则相对于当前位置移动；否则为绝对位置。默认为 False。
    
    异常:
        KnifeBotError: 如果坐标为空。
    """
    ...

def drag(pos: Tuple[int, int], button: Optional[str] = None) -> None:
    """
    拖动鼠标到指定位置。

    参数:
        pos (Tuple[int, int]): 目标坐标，格式为 (x, y)。
        button (Optional[str]): 要使用的鼠标按钮。默认为 None。

    异常:
        KnifeBotError: 如果坐标为空。
    """
    ...

def click(count: int = 1, interval: int = 0, button: Optional[str] = None) -> None:
    """
    点击鼠标。

    参数:
        count (int): 点击次数。默认为 1。
        interval (int): 点击间隔（毫秒）。默认为 0。
        button (Optional[str]): 要点击的鼠标按钮。默认为 None。
    """
    ...

def press(count: int = 1, interval: int = 0, button: Optional[str] = None) -> None:
    """
    按下鼠标按钮。

    参数:
        count (int): 按下次数。默认为 1。
        interval (int): 按下间隔（毫秒）。默认为 0。
        button (Optional[str]): 要按下的鼠标按钮。默认为 None。
    """
    ...

def release(count: int = 1, interval: int = 0, button: Optional[str] = None) -> None:
    """
    释放鼠标按钮。

    参数:
        count (int): 释放次数。默认为 1。
        interval (int): 释放间隔（毫秒）。默认为 0。
        button (Optional[str]): 要释放的鼠标按钮。默认为 None。
    """
    ...

def scroll(length: int, horizontal: Optional[bool] = None) -> None:
    """
    滚动鼠标滚轮。

    参数:
        length (int): 滚动的距离。
        horizontal (Optional[bool]): 如果为 True，则水平滚动；否则垂直滚动。默认为 None。
    """
    ...

def get_pos() -> Tuple[int, int]:
    """
    获取当前鼠标位置。

    返回:
        Tuple[int, int]: 当前鼠标坐标，格式为 (x, y)。
    """
    ...