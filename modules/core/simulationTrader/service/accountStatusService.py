from modules.core.entity.AccountStatus import AccountStatus
from modules.core.utils import mysqlUtil


# 查询
def get():
    # 定义要执行的SQL语句
    sql = "SELECT * FROM account_status WHERE account_id=1;"
    # 取到查询结果
    result = mysqlUtil.query(sql)
    if result is ():
        return None

    dataSet = result[0]
    accountStatus = AccountStatus(
        account_id = dataSet[0],
        total_assets = dataSet[1],
        fund_balance = dataSet[2],
        available_fund = dataSet[3],
        stock_market_value = dataSet[4],
        today_profit_loss = dataSet[5],
        today_profit_loss_ratio = dataSet[6],
        position_profit_loss = dataSet[7],
        position_profit_loss_ratio = dataSet[8],
    )

    return accountStatus

# 更新记录
def update(accountStatus):
    # 定义要执行的SQL语句
    sql = 'UPDATE account_status SET ' \
          'total_assets=%s,fund_balance=%s,available_fund=%s,stock_market_value=%s,today_profit_loss=%s,today_profit_loss_ratio=%s,' \
          'position_profit_loss=%s,position_profit_loss_ratio=%s WHERE account_id=1'

    params = [accountStatus.total_assets, accountStatus.fund_balance,
              accountStatus.available_fund,
              accountStatus.stock_market_value, accountStatus.today_profit_loss, accountStatus.today_profit_loss_ratio,
              accountStatus.position_profit_loss, accountStatus.position_profit_loss_ratio]

    result = mysqlUtil.execute(sql, params)
    return result
