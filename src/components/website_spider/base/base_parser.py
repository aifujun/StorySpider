
from common.regular_expression import RegExpression
from spider.base.http_base import RequestBase


class BaseParser(RequestBase):

    @staticmethod
    def extract_url_from_string(string: str) -> list:
        return RegExpression.url_regexp.findall(string)

    def parse(self, *args, **kwargs):
        raise NotImplementedError
