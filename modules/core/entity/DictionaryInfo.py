class DictionaryInfo:

    """数据库字段名常量"""
    # 字典key
    DIC_KEY = "DIC_KEY"
    # 字典value
    DIC_VALUE = "DIC_VALUE"

    """成员变量"""
    dic_key = ""
    dic_value = ""

    """构造方法"""
    def __init__(self,dic_key, dic_value=None):
        self.dic_key = dic_key
        self.dic_value = dic_value
