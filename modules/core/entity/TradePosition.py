class TradePosition:

    """数据库字段名常量"""
    # 股票代码
    STOCK_CODE = "STOCK_CODE"
    # 股票名字
    STOCK_NAME = "STOCK_NAME"
    # 持仓数量（股）
    TOTAL_AMOUNT = "TOTAL_AMOUNT"
    # 可卖数量（股）
    CAN_SELL_AMOUNT = "CAN_SELL_AMOUNT"
    # 成本价格
    COST_PRICE = "COST_PRICE"
    # 当前价
    CURRENT_PRICE = "CURRENT_PRICE"
    # 浮动盈亏金额
    PL = "PL"
    # 浮动盈亏比例
    PL_RATION = "PL_RATION"
    # 当日浮动盈亏金额
    TODAY_PL = "TODAY_PL"
    # 当日浮动盈亏比例
    TODAY_PL_RATION = "TODAY_PL_RATION"
    # 最新市值
    LATEST_MARKET_VALUE = "LATEST_MARKET_VALUE"

    """成员变量"""
    stock_code = ""
    stock_name = ""
    total_amount = ""
    can_sell_amount = ""
    cost_price = ""
    current_price = ""
    pl = ""
    pl_ration = ""
    today_pl = ""
    today_pl_ration = ""
    latest_market_value = ""

    """构造方法"""
    def __init__(self, stock_code, stock_name=None,total_amount=None, can_sell_amount=None, cost_price=None, current_price=None, pl=None, pl_ration=None,today_pl=None,
                 today_pl_ration=None,latest_market_value=None):
        self.stock_code = stock_code
        self.stock_name = stock_name
        self.total_amount = total_amount
        self.can_sell_amount = can_sell_amount
        self.cost_price = cost_price
        self.current_price = current_price
        self.pl = pl
        self.pl_ration = pl_ration
        self.today_pl = today_pl
        self.today_pl_ration = today_pl_ration
        self.latest_market_value = latest_market_value

    def __str__(self):
        print(self)
