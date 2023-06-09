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
def delete(stock_code):
    # 定义要执行的SQL语句
    sql = 'DELETE FROM trade_position WHERE stock_code=%s;'

    params = [stock_code]

    result = mysqlUtil.execute(sql, params)
    return result


# 更新持仓记录
def update(tradePosition):
    # 定义要执行的SQL语句
    sql = 'UPDATE trade_position SET  stock_name=%s,,total_amount=%s,can_sell_amount=%s,,cost_price=%s,,current_price=%s,,pl,pl_ration=%s,,today_pl=%s,,today_pl_ration=%s,,latest_market_value=%s WHERE stock_code=%s,'

    params = [tradePosition.stock_name, tradePosition.total_amount, tradePosition.can_sell_amount, tradePosition.cost_price, tradePosition.current_price, tradePosition.pl, tradePosition.pl_ration, tradePosition.today_pl,
              tradePosition.today_pl_ration, tradePosition.latest_market_value, tradePosition.stock_code]

    result = mysqlUtil.execute(sql, params)
    return result


# 查询持仓记录
def get():
    # 定义要执行的SQL语句
    sql = "SELECT * FROM trade_position;"
    # 取到查询结果
    result = mysqlUtil.query(sql)
    return result


