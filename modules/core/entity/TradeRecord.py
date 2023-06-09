class TradeRecord:

    """数据库字段名常量"""
    # ID
    ID = "ID"
    # 股票代码
    STOCK_CODE = "STOCK_CODE"
    # 股票名字
    STOCK_NAME = "STOCK_NAME"
    # 交易时5档详情
    DETAIL = "DETAIL"
    # 交易类型(买入:buy 卖出:sell)
    TRADE_TYPE = "TRADE_TYPE"
    # 交易价格
    TRADE_PRICE = "TRADE_PRICE"
    # 交易数量
    TRADE_AMOUNT = "TRADE_AMOUNT"
    # 交易时间
    TIMESTAMP = "TIMESTAMP"
    # 是否处理到持仓 0未处理  1已处理
    PROCESS_FLAG = "PROCESS_FLAG"

    """成员变量"""
    id = ""
    stock_code = ""
    stock_name = ""
    detail = ""
    trade_type = ""
    trade_price = ""
    trade_amount = ""
    timestamp = ""
    process_flag = ""

    """构造方法"""
    def __init__(self, id=None, stock_code=None, stock_name=None, detail=None, trade_price=None, trade_type=None, trade_amount=None, timestamp=None, process_flag=0):
        self.id = id
        self.stock_code = stock_code
        self.stock_name = stock_name
        self.detail = detail
        self.trade_type = trade_type
        self.trade_price = trade_price
        self.trade_amount = trade_amount
        self.timestamp = timestamp
        self.process_flag = process_flag

