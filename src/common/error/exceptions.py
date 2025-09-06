import ctypes


class ConfigError(Exception):
    def __init__(self, msg: str = None, msg_detail: str = None, *args, **kwargs):
        self.err_msg = msg
        self.err_msg_detail = msg_detail


class WindowsAPIException(RuntimeError):
    def __init__(self, message):
        message = f"{message} {ctypes.WinError()}"
        super(WindowsAPIException, self).__init__(message)


class HttpCodeException(Exception):

    def __init__(self, code: int = None, msg: str = None, msg_detail: str = None, *args, **kwargs):
        self.code = code
        self.err_msg = msg
        self.err_msg_detail = msg_detail


class RequiredParamException(Exception):

    def __init__(self, msg: str = None, msg_detail: str = None, *args, **kwargs):
        self.err_msg = msg
        self.err_msg_detail = msg_detail

