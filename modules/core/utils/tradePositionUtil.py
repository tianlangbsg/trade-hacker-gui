from modules.core.common import common_variables
from modules.core.entity.TradePosition import TradePosition
from modules.core.simulationTrader.service import tradePositionService, tradeRecordService
import modules.core.utils.logUtil as log


# 根据持仓表，计算最新市值，并更新到数据库中
def calc_latest_market_value():
    # 获取持仓信息
    tradePositionS= tradePositionService.getAll()
    # return easyquotation.helpers.get_stock_type(stockCode) + stockCode


# 根据交易记录，将最新持仓信息更新到持仓表
def refresh_trade_positions():
    # 从数据库取得当天交易记录
    tradeRecordList = tradeRecordService.getTodayRecords()
    for tradeRecord in tradeRecordList:
        if tradeRecord.process_flag == 1:
            continue
        # 从持仓表中获取该条记录
        tradePosition = tradePositionService.get(tradeRecord.stock_code)
        # 如果没有该条持仓记录，则追加
        if tradePosition is None and tradeRecord.trade_type == 'buy':
            # 首次买入处理
            tradePosition = TradePosition(
                stock_code=tradeRecord.stock_code,
                stock_name=tradeRecord.stock_name,
                total_amount=tradeRecord.trade_amount,
                can_sell_amount=0,
                cost_price=tradeRecord.trade_price,
                current_price=common_variables.stockRealDict[tradeRecord.stock_code]['now'],
                pl=(float(common_variables.stockRealDict[tradeRecord.stock_code]['now'])-float(tradeRecord.trade_price))*tradeRecord.trade_amount,
                pl_ration=(float(common_variables.stockRealDict[tradeRecord.stock_code]['now'])-float(tradeRecord.trade_price))/float(tradeRecord.trade_price),
                today_pl=0,
                today_pl_ration=0,
                latest_market_value=float(common_variables.stockRealDict[tradeRecord.stock_code]['now'])*tradeRecord.trade_amount,
            )
            tradePositionService.insert(tradePosition)
        # 已有持仓，进行买入处理
        elif tradePosition is not None and tradeRecord.trade_type == 'buy':

            # 先更新成本价
            tradePosition.cost_price = (tradePosition.cost_price*tradePosition.total_amount + tradeRecord.trade_price*tradeRecord.trade_amount)/(tradePosition.total_amount+tradeRecord.trade_amount)
            # 再更新持仓数
            tradePosition.total_amount = tradePosition.total_amount + tradeRecord.trade_amount
            tradePosition.current_price = common_variables.stockRealDict[tradeRecord.stock_code]['now']
            # 计算利润
            tradePosition.pl = (tradePosition.current_price - tradePosition.cost_price)*tradePosition.total_amount
            tradePosition.pl_ration = tradePosition.pl/(tradePosition.cost_price*tradePosition.total_amount)
            tradePosition.latest_market_value = tradePosition.current_price*tradePosition.total_amount

            tradePositionService.update(tradePosition)
        # 已有持仓，进行卖出处理
        elif tradePosition is not None and tradeRecord.trade_type == 'sell':
            # 先更新成本价
            tradePosition.cost_price = (tradePosition.cost_price*tradePosition.total_amount - tradeRecord.trade_price*tradeRecord.trade_amount)/(tradePosition.total_amount-tradeRecord.trade_amount)
            # 再更新持仓数
            tradePosition.total_amount = tradePosition.total_amount - tradeRecord.trade_amount
            tradePosition.current_price = common_variables.stockRealDict[tradeRecord.stock_code]['now']
            # 计算利润
            tradePosition.pl = (tradePosition.current_price - tradePosition.cost_price)*tradePosition.total_amount
            tradePosition.pl_ration = tradePosition.pl/(tradePosition.cost_price*tradePosition.total_amount)
            tradePosition.latest_market_value = tradePosition.current_price*tradePosition.total_amount

            tradePositionService.update(tradePosition)

        # 更新标记，该记录已处理
        tradeRecord.process_flag = 1
        tradeRecordService.update(tradeRecord)
        # 打印日志
        log.info("更新持仓:" + tradeRecord.stock_code + "_" + tradeRecord.stock_name)

