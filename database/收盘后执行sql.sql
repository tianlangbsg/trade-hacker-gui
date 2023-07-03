-- 每日收盘执行一次
-- 持仓记录插入到历史表
INSERT  INTO trade_position_history SELECT *,DATE_FORMAT(NOW(), '%Y%m%d')  FROM trade_position WHERE trade_position.total_amount=0;
-- 清空已清仓股票
DELETE FROM trade_position WHERE trade_position.total_amount=0;
-- 刷新当天的可卖数量=总数量(每天9点前执行一次)
UPDATE trade_position SET can_sell_amount=total_amount WHERE 1=1;
-- 清空没有持仓的股票(每天9点前执行一次)
DELETE FROM  trade_position  WHERE total_amount=0;