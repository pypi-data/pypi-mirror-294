from typing import List, Any

# Ctx 浏览器上下文
class Ctx:
    ...

class Element:
    """
    表示网页中的一个元素。
    提供了查找、等待、点击和发送按键等操作方法。
    """

    def __init__(self, ctx: Ctx, selector: str, by: str = "css") -> None:
        """
        初始化 Element 对象。

        :param ctx: 浏览器上下文
        :param selector: 用于定位元素的选择器
        :param by: 选择器类型，默认为 "css"
        """

    def exist(self) -> bool:
        """
        检查元素是否存在。

        :return: 如果元素存在返回 True，否则返回 False
        """

    def wait(self, timeout: int = 10, delay: int = 100) -> 'Element':
        """
        等待元素出现。

        :param timeout: 超时时间（秒），默认为 10 秒
        :param delay: 每次检查的间隔时间（毫秒），默认为 100 毫秒
        :return: 如果元素出现，返回 self；否则抛出 KnifeBotError
        """

    def click(self) -> 'Element':
        """
        点击元素。

        :return: self，用于链式调用
        """

    def send_text(self, key: str) -> 'Element':
        """
        向元素发送文本。

        :param key: 要发送的文本
        :return: self，用于链式调用
        """

    def send_keys(self, key: List[str]) -> 'Element':
        """
        向元素发送一系列按键。

        :param key: 要发送的按键列表
        :return: self，用于链式调用
        """

class Browser:
    """
    表示一个浏览器实例。
    提供了导航、前进、后退和查找元素等操作方法。
    """

    def __init__(self, url: str = "", timeout: int = 10) -> None:
        """
        初始化 Browser 对象。

        :param url: 初始 URL，默认为空字符串
        :param timeout: 超时时间（秒），默认为 10 秒
        """

    def navigate(self, url: str) -> None:
        """
        导航到指定 URL。

        :param url: 要导航到的 URL
        """

    def back(self) -> None:
        """
        返回上一页。
        """

    def forward(self) -> None:
        """
        前进到下一页。
        """

    def element(self, selector: str, by: str = "css") -> Element:
        """
        查找并返回一个元素。

        :param selector: 用于定位元素的选择器
        :param by: 选择器类型，默认为 "css"
        :return: Element 对象
        """

def create(url: str = "", timeout: int = 10) -> Browser:
    """
    创建并返回一个新的 Browser 实例。

    :param url: 初始 URL，默认为空字符串
    :param timeout: 超时时间（秒），默认为 10 秒
    :return: Browser 对象
    """