-- --------------------------------------------------------
-- 主机:                           iot.taginator.cn
-- 服务器版本:                        8.0.28 - MySQL Community Server - GPL
-- 服务器操作系统:                      Linux
-- HeidiSQL 版本:                  11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- 导出  表 stock_auto.alternative_stock_pool 结构
CREATE TABLE IF NOT EXISTS `alternative_stock_pool` (
  `stock_code` varchar(50) DEFAULT NULL,
  `stock_name` varchar(50) DEFAULT NULL,
  `buy` varchar(50) DEFAULT NULL,
  `sell` varchar(50) DEFAULT NULL,
  `now` varchar(50) DEFAULT NULL,
  `open` varchar(50) DEFAULT NULL,
  `close` varchar(50) DEFAULT NULL,
  `high` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `low` varchar(50) DEFAULT NULL,
  `turnover` varchar(50) DEFAULT NULL,
  `volume` varchar(50) DEFAULT NULL,
  `ask1` varchar(50) DEFAULT NULL,
  `ask1_volume` varchar(50) DEFAULT NULL,
  `ask2` varchar(50) DEFAULT NULL,
  `ask2_volume` varchar(50) DEFAULT NULL,
  `ask3` varchar(50) DEFAULT NULL,
  `ask3_volume` varchar(50) DEFAULT NULL,
  `ask4` varchar(50) DEFAULT NULL,
  `ask4_volume` varchar(50) DEFAULT NULL,
  `ask5` varchar(50) DEFAULT NULL,
  `ask5_volume` varchar(50) DEFAULT NULL,
  `bid1` varchar(50) DEFAULT NULL,
  `bid1_volume` varchar(50) DEFAULT NULL,
  `bid2` varchar(50) DEFAULT NULL,
  `bid2_volume` varchar(50) DEFAULT NULL,
  `bid3` varchar(50) DEFAULT NULL,
  `bid3_volume` varchar(50) DEFAULT NULL,
  `bid4` varchar(50) DEFAULT NULL,
  `bid4_volume` varchar(50) DEFAULT NULL,
  `bid5` varchar(50) DEFAULT NULL,
  `bid5_volume` varchar(50) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  `timestamp` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 数据导出被取消选择。

-- 导出  表 stock_auto.history_data 结构
CREATE TABLE IF NOT EXISTS `history_data` (
  `stock_code` varchar(255) NOT NULL COMMENT '股票代码',
  `date` datetime DEFAULT NULL COMMENT '日期',
  `open` float(255,0) DEFAULT NULL COMMENT '开盘价',
  `high` float(255,0) DEFAULT NULL COMMENT '最高价',
  `close` float(255,0) DEFAULT NULL COMMENT '收盘价',
  `low` float(255,0) DEFAULT NULL COMMENT '最低价',
  `volume` float(255,0) DEFAULT NULL COMMENT '成交量',
  `price_change` float(255,0) DEFAULT NULL COMMENT '价格变动',
  `p_change` float(255,0) DEFAULT NULL COMMENT '涨跌幅',
  `ma5` float(255,0) DEFAULT NULL COMMENT '5日均价',
  `ma10` float(255,0) DEFAULT NULL COMMENT '10日均价',
  `ma20` float(255,0) DEFAULT NULL COMMENT '20日均价',
  `v_ma5` float(255,0) DEFAULT NULL COMMENT '5日均量',
  `v_ma10` float(255,0) DEFAULT NULL COMMENT '10日均量',
  `v_ma20` float(255,0) DEFAULT NULL COMMENT '20日均量',
  `turnover` float(255,0) DEFAULT NULL COMMENT '换手率'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- 数据导出被取消选择。

-- 导出  表 stock_auto.stock_info 结构
CREATE TABLE IF NOT EXISTS `stock_info` (
  `stock_code` varchar(255) NOT NULL,
  `stock_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`stock_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- 数据导出被取消选择。

-- 导出  表 stock_auto.tick_data 结构
CREATE TABLE IF NOT EXISTS `tick_data` (
  `stock_code` varchar(10) NOT NULL COMMENT '股票代码',
  `stock_name` varchar(255) DEFAULT NULL COMMENT '股票名称',
  `buy` float(255,0) DEFAULT NULL COMMENT '竞买价',
  `sell` float(255,0) DEFAULT NULL COMMENT '竞卖价',
  `now` float(255,0) DEFAULT NULL COMMENT '现价',
  `open` float(255,0) DEFAULT NULL COMMENT '开盘价',
  `close` float(255,0) DEFAULT NULL COMMENT '昨日收盘价',
  `high` float(255,0) DEFAULT NULL COMMENT '今日最高价',
  `low` float(255,0) DEFAULT NULL COMMENT '今日最低价',
  `turnover` float(255,0) DEFAULT NULL COMMENT '交易股数',
  `volume` float(255,0) DEFAULT NULL COMMENT '交易金额',
  `ask1` float(255,0) DEFAULT NULL COMMENT '卖一价',
  `ask1_volume` float(255,0) DEFAULT NULL COMMENT '卖一量',
  `ask2` float(255,0) DEFAULT NULL COMMENT '卖二价',
  `ask2_volume` float(255,0) DEFAULT NULL COMMENT '卖二量',
  `ask3` float(255,0) DEFAULT NULL COMMENT '卖三价',
  `ask3_volume` float(255,0) DEFAULT NULL COMMENT '卖三量',
  `ask4` float(255,0) DEFAULT NULL COMMENT '卖四价',
  `ask4_volume` float(255,0) DEFAULT NULL COMMENT '卖四量',
  `ask5` float(255,0) DEFAULT NULL COMMENT '卖五价',
  `ask5_volume` float(255,0) DEFAULT NULL COMMENT '卖五量',
  `bid1` float(255,0) DEFAULT NULL COMMENT '买一价',
  `bid1_volume` float(255,0) DEFAULT NULL COMMENT '买一量',
  `bid2` float(255,0) DEFAULT NULL COMMENT '买二价',
  `bid2_volume` float(255,0) DEFAULT NULL COMMENT '买二量',
  `bid3` float(255,0) DEFAULT NULL COMMENT '买三价',
  `bid3_volume` float(255,0) DEFAULT NULL COMMENT '买三量',
  `bid4` float(255,0) DEFAULT NULL COMMENT '买四价',
  `bid4_volume` float(255,0) DEFAULT NULL COMMENT '买四量',
  `bid5` float(255,0) DEFAULT NULL COMMENT '买五价',
  `bid5_volume` float(255,0) DEFAULT NULL COMMENT '买五量',
  `date` varchar(18) DEFAULT NULL COMMENT '日期',
  `time` varchar(18) DEFAULT NULL COMMENT '时间',
  `timestamp` datetime DEFAULT NULL COMMENT '时间戳'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- 数据导出被取消选择。

-- 导出  表 stock_auto.trade_record 结构
CREATE TABLE IF NOT EXISTS `trade_record` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '交易id',
  `stock_code` varchar(10) DEFAULT NULL COMMENT '股票代码',
  `stock_name` varchar(20) DEFAULT NULL COMMENT '股票名称',
  `detail` varchar(255) DEFAULT NULL COMMENT '交易时5档详情',
  `trade_price` varchar(255) DEFAULT NULL COMMENT '交易价格',
  `trade_amount` varchar(255) DEFAULT NULL COMMENT '交易数量',
  `timestamp` timestamp NULL DEFAULT NULL COMMENT '交易日期',
  `trade_type` varchar(50) DEFAULT NULL COMMENT '交易类型',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=462 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- 数据导出被取消选择。

-- 导出  表 stock_auto.trade_stock_position 结构
CREATE TABLE IF NOT EXISTS `trade_stock_position` (
  `date` varchar(12) DEFAULT NULL COMMENT '日期',
  `stock_code` varchar(255) DEFAULT NULL COMMENT '股票代码',
  `stock_name` varchar(255) DEFAULT NULL COMMENT '股票名',
  `stock_amount` int DEFAULT NULL COMMENT '持仓数量（股）',
  `can_sell_amount` int DEFAULT NULL COMMENT '可买数量（股）',
  `cost_price` float(20,2) DEFAULT NULL COMMENT '成本价格',
  `current_price` float(20,2) DEFAULT NULL COMMENT '当前价',
  `pl` float(20,0) DEFAULT NULL COMMENT '浮动盈亏金额',
  `pl_ration` float(20,0) DEFAULT NULL COMMENT '浮动盈亏比例',
  `latest_market_value` float(255,0) DEFAULT NULL COMMENT '最新市值'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- 数据导出被取消选择。

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
