from enum import Enum


class ErrorCode(Enum):
    """
    错误码起始保留: 16777216 = 0x1000000

    1) 内部错误(100): 16777217 ~ 16777316
    2) 参数错误(10): 16777317 ~ 16777326
    """
    SUCCESS = 0

    # 内部错误
    INTERNAL_ERROR = 16777217

    # 参数错误
    PARAM_ERROR = 16777317

    # 不允许的传参
    PARAM_NOT_ALLOWED = 16777318

    # 不合法参数
    PARAM_ILLEGAL = 16777319


class HttpStatusCode(int, Enum):
    # 成功
    OK = 200

    # 无法解析此请求
    BAD_REQUEST = 400

    # 请求未经授权
    UNAUTHORIZED = 401

    # 服务器拒绝提供服务
    FORBIDDEN = 403

    # 请求资源不存在
    NOT_FOUND = 404

    METHOD_NOT_ALLOWED = 405

    # 服务器内部错误
    INTERNAL_SERVER_ERROR = 500

    # 服务器不支持该请求中使用的方法
    IMPLEMENTED = 501

    # 网关错误
    BAD_GATEWAY = 502

    # 服务器当前不可用
    SERVER_UNAVAILABLE = 503

    # 网关超时
    GATEWAY_TIMEOUT = 504

