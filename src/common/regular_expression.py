
import re


class RegExpression:
    r"""
    正则表达式 -> re.RegexObject

    正则表达式`flags`:
        1) re.I(IGNORECASE): 忽略大小写
        2) re.M(MULTILINE): 多行模式，改变`^`和`$`的行为
        3) re.S(DOTALL): 点任意匹配模式，改变`.`的行为（使`.`能匹配换行符）
        4) re.L(LOCALE): 使预定字符类 \w \W \b \B \s \S 取决于当前区域设定
        5) re.U(UNICODE): 使预定字符类 \w \W \b \B \s \S \d \D 取决于unicode定义的字符属性
        6) re.X(VERBOSE): 详细模式。这个模式下正则表达式可以是多行，忽略空白字符，并可以加入注释`#`
    """

    # URL正则提取
    # url_regexp = re.compile(r'((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)'
    #                         r'(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+'
    #                         r'(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
    #                         re.IGNORECASE)
    # url_regexp = re.compile(r'https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    url_regexp = re.compile(
        '(?:https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;\u4E00-\u9FA5]+[-A-Za-z0-9+&@#/%=~_|\u4E00-\u9FA5]')

    douyin_render_data = re.compile('(?<=id="RENDER_DATA" type="application/json">)(.*?)(?=</script>)', re.DOTALL)

    content_desc_filename = re.compile('(?<=filename=").*(?=")')
