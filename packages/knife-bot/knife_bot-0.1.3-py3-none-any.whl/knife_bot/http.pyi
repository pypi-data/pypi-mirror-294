from typing import Optional, Dict

class Response:
    """
    HTTP 请求响应。

    属性:
    code -- 响应码
    body -- 响应体
    cookie -- 响应cookie
    """
    code: int
    body: str
    cookie: str
    ...

def get(url: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, str]] = None) -> Response:
    """
    执行 GET 请求。

    参数:
    url -- 请求的URL
    headers -- 可选，请求头字典
    params -- 可选，URL参数字典
    """
    ...

def head(url: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, str]] = None) -> Response:
    """
    执行 HEAD 请求。

    参数:
    url -- 请求的URL
    headers -- 可选，请求头字典
    params -- 可选，URL参数字典
    """
    ...

def options(url: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, str]] = None) -> Response:
    """
    执行 OPTIONS 请求。

    参数:
    url -- 请求的URL
    headers -- 可选，请求头字典
    params -- 可选，URL参数字典
    """
    ...

def trace(url: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, str]] = None) -> Response:
    """
    执行 TRACE 请求。

    参数:
    url -- 请求的URL
    headers -- 可选，请求头字典
    params -- 可选，URL参数字典
    """
    ...

def post(url: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, str]] = None, data: Optional[Dict[str, str]] = None) -> Response:
    """
    执行 POST 请求。

    参数:
    url -- 请求的URL
    headers -- 可选，请求头字典
    params -- 可选，URL参数字典
    data -- 可选，请求体数据字典
    """
    ...

def put(url: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, str]] = None, data: Optional[Dict[str, str]] = None) -> Response:
    """
    执行 PUT 请求。

    参数:
    url -- 请求的URL
    headers -- 可选，请求头字典
    params -- 可选，URL参数字典
    data -- 可选，请求体数据字典
    """
    ...

def patch(url: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, str]] = None, data: Optional[Dict[str, str]] = None) -> Response:
    """
    执行 PATCH 请求。

    参数:
    url -- 请求的URL
    headers -- 可选，请求头字典
    params -- 可选，URL参数字典
    data -- 可选，请求体数据字典
    """
    ...

def delete(url: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, str]] = None, data: Optional[Dict[str, str]] = None) -> Response:
    """
    执行 DELETE 请求。

    参数:
    url -- 请求的URL
    headers -- 可选，请求头字典
    params -- 可选，URL参数字典
    data -- 可选，请求体数据字典
    """
    ...

def request(
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, str]] = None,
    data: Optional[Dict[str, str]] = None
) -> Response:
    """
    使用指定的方法执行 HTTP 请求。

    参数:
    method -- HTTP请求方法
    url -- 请求的URL
    headers -- 可选，请求头字典
    params -- 可选，URL参数字典
    data -- 可选，请求体数据字典
    """
    ...