from modules.core.entity.TradePosition import TradePosition
from modules.core.entity.TradeRecord import TradeRecord
from modules.core.utils import mysqlUtil


def getAll():
    # 定义要执行的SQL语句
    sql = """
          SELECT * FROM trade_record
          """
    # 取到查询结果
    result = mysqlUtil.query(sql)
    return result


# 查询指定日期全部交易记录
def getByDate(date):
    # 定义要执行的SQL语句
    sql = "SELECT * FROM trade_record WHERE trade_type='buy' AND DATE_FORMAT(timestamp, '%Y%m%d')='"+date+"' AND DATE_FORMAT(timestamp, '%H:%i:%S')<'14:57:00';"
    # 取到查询结果
    records = mysqlUtil.query(sql)
    tradeRecordDict = {}
    for dataSet in records:
        stockData = {}
        stockData['id'] = dataSet[0]
        stockData['stock_code'] = dataSet[1]
        stockData['stock_name'] = dataSet[2]
        stockData['detail'] = dataSet[3]
        stockData['trade_price'] = dataSet[4]
        stockData['trade_amount'] = dataSet[5]
        stockData['timestamp'] = dataSet[6]
        stockData['trade_type'] = dataSet[7]
        stockData['trade_record'] = dataSet[8]
        tradeRecordDict[dataSet[1]] = stockData
    return tradeRecordDict


# 查询当天全部交易记录详情
# def getTodayRecords():
#     # 定义要执行的SQL语句
#     sql = "SELECT *,trade_price*trade_amount AS money FROM trade_record WHERE DATE_FORMAT(timestamp, '%Y%m%d')=DATE_FORMAT(NOW(), '%Y%m%d') ORDER BY TIMESTAMP ASC;"
#     # 取到查询结果
#     records = mysqlUtil.query(sql)
#     tradeRecordDict = {}
#     for dataSet in records:
#         stockData = {}
#         stockData['id'] = dataSet[0]
#         stockData['stock_code'] = dataSet[1]
#         stockData['stock_name'] = dataSet[2]
#         stockData['detail'] = dataSet[3]
#         stockData['trade_price'] = dataSet[4]
#         stockData['trade_amount'] = dataSet[5]
#         stockData['timestamp'] = dataSet[6]
#         stockData['trade_type'] = dataSet[7]
#         stockData['money'] = dataSet[8]
#         tradeRecordDict[dataSet[1]] = stockData
#     return tradeRecordDict
def getTodayRecords():
    # 定义要执行的SQL语句
    sql = "SELECT * FROM trade_record WHERE DATE_FORMAT(timestamp, '%Y%m%d')=DATE_FORMAT(NOW(), '%Y%m%d') ORDER BY TIMESTAMP ASC;"
    # 取到查询结果
    records = mysqlUtil.query(sql)
    tradeRecordList = []
    for dataSet in records:
        tradeRecord = TradeRecord(
            id=dataSet[0],
            stock_code=dataSet[1],
            stock_name=dataSet[2],
            detail=dataSet[3],
            trade_price=float(dataSet[4]),
            trade_amount=int(dataSet[5]),
            timestamp=dataSet[6],
            trade_type=dataSet[7],
            process_flag=dataSet[8],
        )
        tradeRecordList.append(tradeRecord)
    return tradeRecordList


# 查询指定日期全部股票
def getStocksByDate(date, tradeType):
    # 定义要执行的SQL语句
    sql = "SELECT stock_code FROM trade_record WHERE trade_type='"+tradeType+"' AND DATE_FORMAT(timestamp, '%Y%m%d')='"+date+"' AND DATE_FORMAT(timestamp, '%H:%i:%S')<'14:57:00';"
    # 取到查询结果
    result = mysqlUtil.query(sql)
    return result


# 查询指定日期是否存在指定股票的交易记录 buy
def getBuyRecords(date, stockCode):
    # 定义要执行的SQL语句
    sql = "SELECT * FROM trade_record WHERE trade_type='buy' AND stock_code='"+stockCode+"' AND DATE_FORMAT(timestamp, '%Y%m%d')='"+date+"';"
    # 取到查询结果
    result = mysqlUtil.query(sql)
    return result


# 查询指定日期是否存在指定股票的交易记录 sell
def getSellRecords(date, stockCode):
    # 定义要执行的SQL语句
    sql = "SELECT * FROM trade_record WHERE trade_type='sell' AND stock_code='"+stockCode+"' AND DATE_FORMAT(timestamp, '%Y%m%d')='"+date+"';"
    # 取到查询结果
    result = mysqlUtil.query(sql)
    return result


# 查询指定日期的总资产
def getTotalAssetsByDate(date):
    # 定义要执行的SQL语句
    sql = "SELECT SUM(t.money) AS total_money FROM (SELECT *,trade_price*trade_amount AS money FROM trade_record WHERE DATE_FORMAT(timestamp, '%Y%m%d')='" + date + "' AND DATE_FORMAT(timestamp, '%H:%i:%S')<'14:57:00') AS t;"
    # 取到查询结果
    result = mysqlUtil.query(sql)
    return result


def insert(tradeRecord):
    # 定义要执行的SQL语句
    sql = 'INSERT INTO trade_record (stock_code,stock_name,detail,trade_type,trade_price,trade_amount,timestamp,process_flag) ' \
          'VALUES (%s,%s,%s,%s,%s,%s,%s,%s);'

    params = [tradeRecord.stock_code, tradeRecord.stock_name, tradeRecord.detail, tradeRecord.trade_type, tradeRecord.trade_price, tradeRecord.trade_amount,tradeRecord.timestamp,tradeRecord.process_flag]

    result = mysqlUtil.execute(sql, params)
    return result


def update(tradeRecord):
    # 定义要执行的SQL语句
    sql = 'UPDATE trade_record SET stock_code=%s,stock_name=%s,detail=%s,trade_type=%s,trade_price=%s,trade_amount=%s,timestamp=%s,process_flag=%s WHERE id=%s;'

    params = [tradeRecord.stock_code, tradeRecord.stock_name, tradeRecord.detail, tradeRecord.trade_type, tradeRecord.trade_price, tradeRecord.trade_amount,tradeRecord.timestamp,tradeRecord.process_flag,tradeRecord.id]

    result = mysqlUtil.execute(sql, params)
    return result
