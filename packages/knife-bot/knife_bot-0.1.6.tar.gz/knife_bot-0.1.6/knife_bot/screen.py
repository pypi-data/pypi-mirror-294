from typing import Tuple, Optional

def screenshot(path: str, area: Optional[Tuple[int, int, int, int]] = None) -> bool:
    """
    截取屏幕截图并保存到指定路径。

    参数:
        path (str): 保存截图的文件路径。
        area (Optional[Tuple[int, int, int, int]]): 截图区域，格式为 (x, y, width, height)。默认为 None，表示全屏。

    返回:
        bool: 截图是否成功。
    """
    ...

def find_pic(
    img: str,
    area: Optional[Tuple[int, int, int, int]] = None,
    mode: str = "center",
    threshold: float = 0.9,
) -> Optional[Tuple[int, int]]:
    """
    在屏幕上查找指定图片。

    参数:
        img (str): 要查找的图片路径或图片base64编码。
        area (Optional[Tuple[int, int, int, int]]): 查找区域，格式为 (x, y, width, height)。默认为 None，表示全屏。
        mode (str): 返回坐标的模式，可选值为 "leftTop", "leftBottom", "center", "rightTop", "rightBottom"。默认为 "center"。
        threshold (float): 匹配阈值，范围为 0-1。默认为 0.9。

    返回:
        Optional[Tuple[int, int]]: 如果找到图片，返回指定模式的坐标；否则返回 None。

    异常:
        KnifeBotError: 如果输入的图片路径为空。
    """
    ...