from modules.core.entity.AccountStatus import AccountStatus
from modules.core.entity.TradePosition import TradePosition
from modules.core.simulationTrader.service import accountStatusService
from modules.core.utils import mysqlUtil


# 插入持仓记录
def insert(tradePosition):
    # 定义要执行的SQL语句
    sql = 'INSERT INTO trade_position (stock_code, stock_name,total_amount, can_sell_amount,cost_price,current_price,pl,pl_ration,today_pl,today_pl_ration,latest_market_value) ' \
          'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'

    params = [tradePosition.stock_code, tradePosition.stock_name, tradePosition.total_amount, tradePosition.can_sell_amount, tradePosition.cost_price, tradePosition.current_price, tradePosition.pl,
              tradePosition.pl_ration, tradePosition.today_pl,tradePosition.today_pl_ration, tradePosition.latest_market_value]

    result = mysqlUtil.execute(sql, params)
    return result


# 删除持仓记录
def delete(stockCode):
    # 定义要执行的SQL语句
    sql = 'DELETE FROM trade_position WHERE stock_code=%s;'

    params = [stockCode]

    result = mysqlUtil.execute(sql, params)
    return result


# 更新持仓记录
def update(tradePosition):
    # 定义要执行的SQL语句
    sql = 'UPDATE trade_position SET  stock_name=%s,total_amount=%s,can_sell_amount=%s,cost_price=%s,current_price=%s,pl=%s,pl_ration=%s,today_pl=%s,today_pl_ration=%s,latest_market_value=%s WHERE stock_code=%s;'

    params = [tradePosition.stock_name, tradePosition.total_amount, tradePosition.can_sell_amount, tradePosition.cost_price, tradePosition.current_price, tradePosition.pl, tradePosition.pl_ration, tradePosition.today_pl,
              tradePosition.today_pl_ration, tradePosition.latest_market_value, tradePosition.stock_code]

    result = mysqlUtil.execute(sql, params)
    return result


# 查询持仓记录
def getAll():
    # 定义要执行的SQL语句
    sql = "SELECT * FROM trade_position;"
    # 取到查询结果
    result = mysqlUtil.query(sql)
    tradePositionList = []
    for dataSet in result:
        tradePosition = TradePosition(
            stock_code=dataSet[0],
            stock_name=dataSet[1],
            total_amount=dataSet[2],
            can_sell_amount=dataSet[3],
            cost_price=dataSet[4],
            current_price=dataSet[5],
            pl=dataSet[6],
            pl_ration=dataSet[7],
            today_pl=dataSet[8],
            today_pl_ration=dataSet[9],
            latest_market_value=dataSet[10],
        )

        tradePositionList.append(tradePosition)
    return tradePositionList


# 查询持仓记录
def getCanSell():
    # 定义要执行的SQL语句
    sql = "SELECT * FROM trade_position WHERE can_sell_amount>0;"
    # 取到查询结果
    result = mysqlUtil.query(sql)
    tradePositionList = []
    for dataSet in result:
        tradePosition = TradePosition(
            stock_code=dataSet[0],
            stock_name=dataSet[1],
            total_amount=dataSet[2],
            can_sell_amount=dataSet[3],
            cost_price=dataSet[4],
            current_price=dataSet[5],
            pl=dataSet[6],
            pl_ration=dataSet[7],
            today_pl=dataSet[8],
            today_pl_ration=dataSet[9],
            latest_market_value=dataSet[10],
        )

        tradePositionList.append(tradePosition)
    return tradePositionList


# 查询持仓记录
def get(stockCode):
    # 定义要执行的SQL语句
    sql = "SELECT * FROM trade_position WHERE stock_code='"+ stockCode + "';"
    # 取到查询结果
    result = mysqlUtil.query(sql)
    if result is ():
        return None

    dataSet = result[0]
    tradePosition = TradePosition(
        stock_code=dataSet[0],
        stock_name=dataSet[1],
        total_amount=dataSet[2],
        can_sell_amount=dataSet[3],
        cost_price=dataSet[4],
        current_price=dataSet[5],
        pl=dataSet[6],
        pl_ration=dataSet[7],
        today_pl=dataSet[8],
        today_pl_ration=dataSet[9],
        latest_market_value=dataSet[10],
    )

    return tradePosition


# test
# # 取得账号状态信息
# accountStatus = accountStatusService.get()
#
# tradePositionList = getAll()
# for tradePosition in tradePositionList:
#
#     # 计算账户余额
#     accountStatus.fund_balance = accountStatus.fund_balance - tradePosition.total_amount*tradePosition.cost_price
#     # 总市值
#     accountStatus.stock_market_value = accountStatus.stock_market_value + tradePosition.total_amount*tradePosition.current_price
#     # 总资产
#     accountStatus.total_assets = accountStatus.fund_balance + accountStatus.stock_market_value
#     # 总盈亏
#     accountStatus.position_profit_loss = accountStatus.position_profit_loss + tradePosition.pl
#     # 总盈亏率
#     accountStatus.position_profit_loss_ratio = accountStatus.position_profit_loss/accountStatus.total_assets
#
# # 更新账户信息到数据库
# accountStatusService.update(accountStatus)


