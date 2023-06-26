import datetime
import operator
import threading
import time
import modules.core.utils.logUtil as log

import easyquotation
# from dbUtil import mysqlUtil
from time import localtime

from modules.core.entity.AlternativeStockPool import AlternativeStockPool
from modules.core.common import common_variables
from modules.core.entity.TradeRecord import TradeRecord
from modules.core.simulationTrader import tradeUtil
from modules.core.simulationTrader.service import alternativeStockPoolService, tradeRecordService, tradePositionService
from modules.core.simulationTrader.tradeUtil import buyStock, sellStock
from modules.core.utils import ig507Util, stockUtil
from modules.core.utils import tushareUtil

quotation = easyquotation.use('tencent')  # 新浪 ['sina'] 腾讯 ['tencent', 'qq']

# *************************************************************************************
# 标准方法
# *************************************************************************************
# *************************************************************************************

# 刷新获取所有股票数组数据，并保存到stockRealDict, key=stock_code
def get_all_real_and_save(stockCodeListList):
    for stockCodeList in stockCodeListList:
        tempDict = quotation.get_stock_data(stockCodeList)
        for key in tempDict.keys():
            stockData = tempDict[key]
            # 如果该票的key不存在，则跳过
            if common_variables.stockHistoryDict.get(key) == None:
                continue
            # 如果该票未开盘，则跳过
            if stockData['now'] == None or common_variables.stockHistoryDict[key]['close'] == None:
                continue
            # 根据上个收盘价，计算当天涨停价格
            stockData['limit_high'] = stockUtil.calc_price_limit_high(common_variables.stockHistoryDict[key]['close'])
            # 根据上个收盘价，计算当天涨停幅度
            stockData['change_range'] = stockUtil.calc_price_change_range(common_variables.stockHistoryDict[key]['close'],
                                                                          stockData['now'])
            common_variables.stockRealDict[key] = stockData


# 刷新获取所有持仓股票数组数据，并保存到stockPositionRealDict, key=stock_code
def get_all_position_real_and_save():

    # 取得当日可卖出的股票列表
    canSellStockList = tradePositionService.getCanSell()
    codeList = []
    canSellDict = {}
    for stockData in canSellStockList:
        codeList.append(stockUtil.get_complete_stock_code(stockData.stock_code))
        canSellDict[stockData.stock_code] = stockData.can_sell_amount
    stockCodeListList = stockUtil.list_split(codeList, 300)

    for stockCodeList in stockCodeListList:
        tempDict = quotation.get_stock_data(stockCodeList)
        for key in tempDict.keys():
            stockData = tempDict[key]
            # 如果该票的key不存在，则跳过
            if common_variables.stockHistoryDict.get(key) == None:
                continue
            # 如果该票未开盘，则跳过
            if stockData['now'] == None or common_variables.stockHistoryDict[key]['close'] == None:
                continue
            # 根据上个收盘价，计算当天涨停价格
            stockData['limit_high'] = stockUtil.calc_price_limit_high(common_variables.stockHistoryDict[key]['close'])
            # 根据上个收盘价，计算当天涨停幅度
            stockData['change_range'] = stockUtil.calc_price_change_range(common_variables.stockHistoryDict[key]['close'],
                                                                          stockData['now'])
            # 计算持仓可卖数量
            stockData['can_sell_amount'] = canSellDict[key]
            common_variables.stockPositionRealDict[key] = stockData


# 刷新获取排名靠前股票数组数据，并保存到stockReal100Dict, key=stock_code
def get_top_real_and_save():
    # global stockRank100List
    # global stockRank100Dict
    if common_variables.stockRank100List.__len__() < 1:
        return
    refreshTopTime = datetime.datetime.now()
    tempDict = quotation.get_stock_data(common_variables.stockRank100List)
    # log.info('Top100行情API获取耗时:' + format((datetime.datetime.now() - refreshTopTime).total_seconds(), '.3f') + 'S')
    common_variables.stockRank100Dict.clear()
    # 获取最新top100分时价格数据
    for key in tempDict.keys():
        stockData = tempDict[key]
        # 如果该票的key不存在，则跳过
        if common_variables.stockHistoryDict.get(key) == None:
            continue
        # 如果该票未开盘，则跳过
        if stockData['now'] == None or common_variables.stockHistoryDict[key]['close'] == None:
            continue
        # 根据上个收盘价，计算当天涨停价格
        stockData['limit_high'] = stockUtil.calc_price_limit_high(common_variables.stockHistoryDict[key]['close'])
        # 根据上个收盘价，计算当天涨停幅度
        stockData['change_range'] = stockUtil.calc_price_change_range(common_variables.stockHistoryDict[key]['close'], stockData['now'])
        # 判断是否濒临涨停（已经涨停的不计入）
        if int(stockData['ask1_volume']) != 0:
            common_variables.stockRank100Dict[key] = stockData
    tempDict.clear()
    log.info('Top100行情刷新耗时:' + format((datetime.datetime.now() - refreshTopTime).total_seconds(), '.3f') + 'S')


# 对涨幅前100的进行排序
def sort_stock_rank100():
    # 按最新涨跌幅排序
    for key in common_variables.stockRealDict.keys():
        try:
            common_variables.stockRankDict[key] = common_variables.stockRealDict[key]['change_range']
        except:
            log.info(common_variables.stockRealDict[key])
            common_variables.stockRealDict[key]['change_range']

    common_variables.stockRankList = sorted(common_variables.stockRankDict.items(), key=operator.itemgetter(1), reverse=True)
    common_variables.stockRank100List.clear()
    for rank in common_variables.stockRankList[0:100]:
        common_variables.stockRank100List.append(stockUtil.get_complete_stock_code(rank[0]))


# *************************************************************************************
# 多线程定时执行任务
# *************************************************************************************
# 定时任务，刷新最新股票价格
def refresh_real_info(stockCodeListList):
    # 获取最新分时价格数据
    while common_variables.homeThreadStatus:
        try:
            refreshTime = datetime.datetime.now()
            # 更新数据键值对
            get_all_real_and_save(stockCodeListList)
            # log.info('全行情API获取耗时' + format((datetime.datetime.now() - refreshTime).total_seconds(), '.3f') + 'S')
            sort_stock_rank100()
            log.info('全行情刷新耗时' + format((datetime.datetime.now() - refreshTime).total_seconds(), '.3f') + 'S')
            refreshTime = datetime.datetime.now()
            time.sleep(60)
        except Exception as e:
            log.error('全行情刷新失败:' + e.__str__())


# 定时任务，刷新接近涨停的前100个股票最新情况
def refresh_top100_info():
    # global stockCodeList
    # 获取最新分时价格数据
    while common_variables.homeThreadStatus:
        try:
            # 更新数据键值对
            get_top_real_and_save()
            time.sleep(1)
        except Exception as ex:
            log.error('Top100刷新错误:' + ex.__str__())


# 定时任务，判断top100股票的实时5档行情，并物色合适的待操作目标
def select_target_from_top100():
    # global stockRank100Dict
    # global candidateList
    while common_variables.homeThreadStatus:
        try:
            time.sleep(1)
            for key in common_variables.stockRank100Dict.keys():

                # 取出单只股票实时数据
                stockData = common_variables.stockRank100Dict[key]
                # 取出单只股票过去60日数据
                stockHistory60Data = common_variables.allStockHistoryDict[key]
                # 判断当前股票是否濒临涨停（ask1在涨停价格上）
                if not stockUtil.is_ask1_at_high_limit(stockData):
                    continue
                # 判断卖一剩余金额是否小于指定数量
                if not stockUtil.ask1_money_less_than_goal(stockData):
                    continue
                # 判断量能是否温和放量
                # if not stockUtil.is_moderate_volume(stockHistory60Data):
                #     continue
                # TODO 判断过去n个交易日内，最高涨幅是否符合1.2倍-1.8倍的区间
                # TODO 判断当前股票当日内的开板次数
                # TODO 判断当天价格是否是30日内的新高，如果不是，计算出与前高的差距
                # TODO 判断板子上的封单数量是否满足，判断卖一是否金额小于500W
                # TODO 判断所属板块的涨幅，以及所属板块是否是热点
                # TODO 根据首次涨停时间、计算连板数量判断是不是龙头？
                # 判断当前股票当日内是否有过涨停
                # if not stockUtil.has_reached_high_limit(stockData):
                #     continue

                # #################################################################################
                alternativeStock = common_variables.candidateList[key] = common_variables.stockRank100Dict[key]
                # 添加到候选股票池
                log.info('选中股票:' + key)
                log.info('实时数据:' + str(common_variables.candidateList[key]))
                # 添加到候选股票池
                alternativeStockPool = AlternativeStockPool(
                    stock_code=alternativeStock["code"],
                    stock_name=alternativeStock["name"],
                    buy=None,
                    sell=None,
                    now=alternativeStock["now"],
                    open=alternativeStock["open"],
                    close=alternativeStock["close"],
                    high=alternativeStock["high"],
                    low=alternativeStock["low"],
                    turnover=alternativeStock["turnover"],
                    volume=alternativeStock["volume"],
                    ask1=alternativeStock["ask1"],
                    ask1_volume=alternativeStock["ask1_volume"],
                    ask2=alternativeStock["ask2"],
                    ask2_volume=alternativeStock["ask2_volume"],
                    ask3=alternativeStock["ask3"],
                    ask3_volume=alternativeStock["ask3_volume"],
                    ask4=alternativeStock["ask4"],
                    ask4_volume=alternativeStock["ask4_volume"],
                    ask5=alternativeStock["ask5"],
                    ask5_volume=alternativeStock["ask5_volume"],
                    bid1=alternativeStock["bid1"],
                    bid1_volume=alternativeStock["bid1_volume"],
                    bid2=alternativeStock["bid2"],
                    bid2_volume=alternativeStock["bid2_volume"],
                    bid3=alternativeStock["bid3"],
                    bid3_volume=alternativeStock["bid3_volume"],
                    bid4=alternativeStock["bid4"],
                    bid4_volume=alternativeStock["bid4_volume"],
                    bid5=alternativeStock["bid5"],
                    bid5_volume=alternativeStock["bid5_volume"],
                    date=datetime.datetime.now().strftime('%Y%m%d'),
                    time=alternativeStock["datetime"],
                    timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                )
                # 插入选股记录
                alternativeStockPoolService.insert(alternativeStockPool)
                # 判断是否在交易时间范围内
                currentTime = datetime.datetime.now().strftime('%H%M%S')
                if("093000" < currentTime < "113000") or ("130000" < currentTime < "145700"):
                    # 计算买入数量（最大不超过1W）
                    buyAmount = int((10000/alternativeStockPool.now)/100)*100
                    # 插入购买记录
                    # 查询当日是否已经购买该票
                    todayTradeRecords = tradeRecordService.getBuyRecords(datetime.datetime.now().strftime('%Y%m%d'),
                                                                         stockData.stock_code)
                    # 模拟买入股票(如果今日已买，就忽略)
                    if todayTradeRecords.__len__() == 0:
                        buyStock(alternativeStockPool, buyAmount)

                # #################################################################################
            log.info('********************************************************************')
            log.info(common_variables.candidateList.keys())
            log.info('********************************************************************')
        except Exception as e:
            log.error('选股失败:' + e.__str__())


# 定时任务，自动执行卖操作
def auto_sell():
    # 获取最新分时价格数据
    while True:
        try:
            refreshTime = datetime.datetime.now()
            # 根据交易记录，刷新最新的持仓信息到数据库汇总
            tradeUtil.refresh_trade_records_to_positions()
            tradeUtil.refresh_trade_positions()
            # 更新数据键值对
            get_all_position_real_and_save()
            for stockCode in common_variables.stockPositionRealDict.keys():
                data = common_variables.stockPositionRealDict[stockCode]

                # 动态止盈止损2%
                if (float(data['high']) - float(data['now']))/float(data['high']) > float(0.02):
                    # 判断是否在交易时间范围内
                    currentTime = datetime.datetime.now().strftime('%H%M%S')
                    # if ("093000" < currentTime < "113000") or ("130000" < currentTime < "145700"):
                    tradeRecord = TradeRecord(
                        stock_code=data['code'],
                        stock_name=data['name'],
                        detail='全仓',
                        trade_price=data['now'],
                        process_flag=0
                    )
                    if common_variables.stockPositionRealDict[stockCode]['can_sell_amount'] > 0:
                        # 全卖出
                        sellAmount = data['can_sell_amount']
                        # 模拟卖出股票（插入卖出记录）
                        sellStock(tradeRecord, sellAmount)
                        common_variables.stockPositionRealDict[stockCode]['can_sell_amount'] = 0

            log.info('持仓行情刷新耗时' + format((datetime.datetime.now() - refreshTime).total_seconds(), '.3f') + 'S')
            refreshTime = datetime.datetime.now()
            time.sleep(1)
        except Exception as e:
            log.error('持仓情刷新失败:' + e.__str__())

# *************************************************************************************
# *************************************************************************************

# *************************************************************************************
# 主要逻辑
# *************************************************************************************
def start():
    startTime = localtime()
    now = datetime.datetime.now()
    today = now.strftime('%Y%m%d')
    delta = datetime.timedelta(days=1)
    # 如果今天是周一，则自动取得上周五的日期
    if(now.weekday()==0):
        delta = datetime.timedelta(days=3)
    yesterday = (now - delta).strftime('%Y%m%d')
    yesterday = '20230621'

    # 查询当前所有正常上市交易的股票列表ig507
    common_variables.stockCodeList = ig507Util.get_main_stock_list_from_ig507_suffix()

    # 取得所有主板股票上个交易日的信息，并保存到stockHistoryDict
    log.info("初始化上个交易日数据...")
    common_variables.stockHistoryDict = stockUtil.get_history_1(yesterday)
    if common_variables.stockHistoryDict is None:
        common_variables.stockHistoryDict = tushareUtil.get_last_day_data(yesterday)
        # 将该对象写入到本地，下次启动时可以直接进行读取
        stockUtil.save_history_1(common_variables.stockHistoryDict, yesterday)
    log.info("上个交易日数据初始化完成!")

    # 查询主板所有股票过去60个交易日的全部日线信息
    log.info("初始化历史k线交易数据...")
    end = today
    delta = datetime.timedelta(days=60)
    start = (now - delta).strftime('%Y%m%d')
    # 先判断当前是否存在最新的日线数据文件
    common_variables.allStockHistoryDict = stockUtil.get_history_60()
    if common_variables.allStockHistoryDict is None:
        common_variables.allStockHistoryDict = tushareUtil.get_all_history(ig507Util.get_main_stock_list_from_ig507(), start, end)
        # 将该对象写入到本地，下次启动时可以直接进行读取
        stockUtil.save_history_60(common_variables.allStockHistoryDict)
    log.info("历史k线交易数据初始化完成!")

    # 初始化今日全部实时行情
    # 切割成固定大小的子数组
    common_variables.stockCodeListList = stockUtil.list_split(common_variables.stockCodeList, 300)
    log.info("初始化今日全行情...")
    get_all_real_and_save(common_variables.stockCodeListList)
    sort_stock_rank100()
    log.info("今日全行情初始化完成!")
    log.info("初始化今日Top100行情...")
    get_top_real_and_save()
    log.info("今日Top100行情初始化完成!")

    # 启动全行情刷新线程
    log.info("启动全行情刷新线程...")
    common_variables.refreshRealThread = threading.Thread(target=refresh_real_info, args=(common_variables.stockCodeListList,))
    common_variables.refreshRealThread.start()

    # 启动top100行情刷新线程
    log.info("启动top100行情刷新线程...")
    common_variables.refreshTop100Thread = threading.Thread(target=refresh_top100_info)
    common_variables.refreshTop100Thread.start()

    # 启动top100选择操作目标线程
    log.info("启动top100选择操作目标线程...")
    common_variables.selectTargetThread = threading.Thread(target=select_target_from_top100)
    common_variables.selectTargetThread.start()

    # 启动买卖操作线程
    log.info("启动卖出操作目标线程...")
    common_variables.autoSellThread = threading.Thread(target=auto_sell)
    common_variables.autoSellThread.start()
    log.info("运行结束")


def stop():
    try:
        common_variables.refreshRealThread.stop()
        common_variables.refreshTop100Thread.stop()
        common_variables.selectTargetThread.stop()
    except Exception as ex:
        log.error(str(ex))



