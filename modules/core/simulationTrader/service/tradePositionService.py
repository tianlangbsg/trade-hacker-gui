from modules.core.entity.TradePosition import TradePosition
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
    tradePositionDict = {}
    for dataSet in result:
        tradePosition = {}
        tradePosition['stock_code']=dataSet[0],
        tradePosition['stock_name']=dataSet[1],
        tradePosition['total_amount']=dataSet[2],
        tradePosition['can_sell_amount']=dataSet[3],
        tradePosition['cost_price']=dataSet[4],
        tradePosition['current_price']=dataSet[5],
        tradePosition['pl']=dataSet[6],
        tradePosition['pl_ration']=dataSet[7],
        tradePosition['today_pl']=dataSet[8],
        tradePosition['today_pl_ration']=dataSet[9],
        tradePosition['latest_market_value']=dataSet[10],
        tradePositionDict[dataSet[0]] = tradePosition
    return tradePositionDict


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

