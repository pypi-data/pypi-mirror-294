from typing import Callable, Any, Optional

class HookManager:
    def __init__(self) -> None:
        """
        初始化 HookManager 实例。
        """
        ...

    def on(self, event: str, cb: Callable[[Any], None]) -> None:
        """
        注册事件监听器。

        :param event: 要监听的事件名称
        :param cb: 当事件触发时调用的回调函数
        """
        ...

    def emit(self, event: str, payload: Any) -> None:
        """
        触发指定事件。

        :param event: 要触发的事件名称
        :param payload: 传递给事件监听器的数据
        """
        ...

    def off(self, event: str, cb: Optional[Callable[[Any], None]] = None) -> None:
        """
        移除事件监听器。

        :param event: 要移除监听器的事件名称
        :param cb: 要移除的特定回调函数，如果为 None 则移除该事件的所有监听器
        """
        ...

    def stop(self) -> None:
        """
        停止 HookManager。
        """
        ...