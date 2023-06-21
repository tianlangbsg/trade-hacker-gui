class AccountStatus:

    """数据库字段名常量"""
    # 总资产
    TOTAL_ASSETS = "TOTAL_ASSETS"
    # 资金金额
    FUND_BALANCE = "FUND_BALANCE"
    # 可用金额
    AVAILABLE_FUND = "AVAILABLE_FUND"
    # 股票市值
    STOCK_MARKET_VALUE = "STOCK_MARKET_VALUE"
    # 当日盈亏
    TODAY_PROFIT_LOSS = "DAY_PROFIT_LOSS"
    # 当日盈亏比
    TODAY_PROFIT_LOSS_RATIO = "DAY_PROFIT_LOSS_RATIO"
    # 持仓盈亏
    POSITION_PROFIT_LOSS = "POSITION_PROFIT_LOSS"
    # 持仓盈亏率
    POSITION_PROFIT_LOSS_RATIO = "POSITION_PROFIT_LOSS"

    """成员变量"""
    total_assets = ""
    fund_balance = ""
    available_fund = ""
    stock_market_value = ""
    today_profit_loss = ""
    today_profit_loss_ratio = ""
    position_profit_loss = ""
    position_profit_loss_ratio = ""

    """构造方法"""
    def __init__(self,account_id=None,total_assets=None,fund_balance=None,available_fund=None,stock_market_value=None,today_profit_loss=None,
                 today_profit_loss_ratio=None,position_profit_loss=None,position_profit_loss_ratio = None):
        self.account_id = account_id
        self.total_assets = total_assets
        self.fund_balance = fund_balance
        self.available_fund = available_fund
        self.stock_market_value = stock_market_value
        self.today_profit_loss = today_profit_loss
        self.today_profit_loss_ratio = today_profit_loss_ratio
        self.position_profit_loss = position_profit_loss
        self.position_profit_loss_ratio = position_profit_loss_ratio

