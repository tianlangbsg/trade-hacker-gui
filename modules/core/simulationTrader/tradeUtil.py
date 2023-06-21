import datetime
from modules.core.entity.TradeRecord import TradeRecord
from modules.core.common import common_variables
from modules.core.entity.TradePosition import TradePosition
from modules.core.simulationTrader.service import tradePositionService, tradeRecordService, accountStatusService
import modules.core.utils.logUtil as log


# 模拟买入股票
def buyStock(stockData, buyAmount):
    tradeRecord = TradeRecord(
        stock_code=stockData.stock_code,
        stock_name=stockData.stock_name,
        detail=stockData.bid1_volume,
        trade_type='buy',
        trade_price=stockData.now,
        trade_amount=buyAmount,
        timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
    )
    # 打印日志
    log.info("卖出:" + tradeRecord.stock_code + "_" + tradeRecord.stock_name)
    return tradeRecordService.insert(tradeRecord)


# 模拟卖出股票
def sellStock(stockData, sellAmount):
    tradeRecord = TradeRecord(
        stock_code=stockData.stock_code,
        stock_name=stockData.stock_name,
        detail=stockData.bid1_volume,
        trade_type='sell',
        trade_price=stockData.now,
        trade_amount=sellAmount,
        timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
        process_flag=0
    )
    # 打印日志
    log.info("卖出:" + tradeRecord.stock_code + "_" + tradeRecord.stock_name)
    return tradeRecordService.insert(tradeRecord)


# 根据交易记录，将最新持仓信息更新到持仓表
def refresh_trade_positions():
    # 从数据库取得当天交易记录
    tradeRecordList = tradeRecordService.getTodayRecords()
    # 取得账号状态信息
    accountStatus = accountStatusService.get()
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
            # 计算账户余额
            accountStatus.fund_balance = accountStatus.fund_balance - tradePosition.total_amount * tradePosition.cost_price
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
            # 计算账户余额
            accountStatus.fund_balance = accountStatus.fund_balance - tradePosition.total_amount * tradePosition.cost_price
        # 已有持仓，进行卖出处理
        elif tradePosition is not None and tradeRecord.trade_type == 'sell':
            # 先更新成本价
            if tradePosition.total_amount > tradeRecord.trade_amount:
                tradePosition.cost_price = (
                                                       tradePosition.cost_price * tradePosition.total_amount - tradeRecord.trade_price * tradeRecord.trade_amount) / (
                                                       tradePosition.total_amount - tradeRecord.trade_amount)
                tradePosition.pl_ration = tradePosition.pl / (tradePosition.cost_price * tradePosition.total_amount)

            # 再更新持仓数
            tradePosition.total_amount = tradePosition.total_amount - tradeRecord.trade_amount
            tradePosition.current_price = common_variables.stockRealDict[tradeRecord.stock_code]['now']
            # 计算利润
            tradePosition.pl = (tradePosition.current_price - tradePosition.cost_price)*tradePosition.total_amount
            tradePosition.latest_market_value = tradePosition.current_price*tradePosition.total_amount

            tradePositionService.update(tradePosition)
            # 计算账户余额
            accountStatus.fund_balance = accountStatus.fund_balance + tradeRecord.trade_amount*tradeRecord.trade_price

        # 更新账户信息（买入卖出部分）
        accountStatusService.update(accountStatus)
        # 更新标记，该记录已处理
        tradeRecord.process_flag = 1
        tradeRecordService.update(tradeRecord)
        # 打印日志
        log.info("更新持仓:" + tradeRecord.stock_code + "_" + tradeRecord.stock_name)


# 计算账户状态
def refresh_account_status():
    # 取得账号状态信息
    accountStatus = accountStatusService.get()
    accountStatus.stock_market_value = float(0)
    accountStatus.position_profit_loss = float(0)

    tradePositionList = tradePositionService.getAll()
    for tradePosition in tradePositionList:
        # 总市值
        accountStatus.stock_market_value = accountStatus.stock_market_value + tradePosition.total_amount * tradePosition.current_price
        # 总盈亏
        accountStatus.position_profit_loss = accountStatus.position_profit_loss + tradePosition.pl

    # 总资产
    accountStatus.total_assets = accountStatus.fund_balance + accountStatus.stock_market_value
    # 总盈亏率
    accountStatus.position_profit_loss_ratio = accountStatus.position_profit_loss / accountStatus.total_assets
    # 更新账户信息到数据库
    accountStatusService.update(accountStatus)
    return accountStatus

