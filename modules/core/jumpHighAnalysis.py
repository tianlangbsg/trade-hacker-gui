import datetime

import numpy as np

import utils.logUtil as log
import matplotlib.pyplot as plt

# pyecharts引用
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line

import easyquotation
# from dbUtil import mysqlUtil
from time import strftime, localtime
from utils import stockUtil
from utils import ig507Util
from utils import tushareUtil
from utils.commonUtil import get_root_path, get_home_path

quotation = easyquotation.use('sina')  # 新浪 ['sina'] 腾讯 ['tencent', 'qq']

# 分析历史时长
dayCount = 120

startTime = localtime()
now = datetime.datetime.now()
today = now.strftime('%Y%m%d')
delta = datetime.timedelta(days=1)
# 如果今天是周一，则自动取得上周五的日期
if(now.weekday()==0):
    delta = datetime.timedelta(days=3)
yesterday = (now - delta).strftime('%Y%m%d')

# 初始化过去60天的全部交易数据
end = today
delta = datetime.timedelta(days=dayCount)
start = (now - delta).strftime('%Y%m%d')

allStockHistoryDict = stockUtil.get_history_60()
if allStockHistoryDict is None:
    allStockHistoryDict = tushareUtil.get_all_history(ig507Util.get_main_stock_list_bare_from_ig507(), start, end)
    # 将该对象写入到本地，下次启动时可以直接进行读取
    stockUtil.save_history_60(allStockHistoryDict)
log.info("历史交易数据初始化完成!")

# 存放分析结果
analysisResult = {}
# 存放历史跳空高开收盘数据
jumpHighLimitDict = {}

rangeLow = 5
rangeHigh = 9

# 遍历所有股票数据
for stockCode in allStockHistoryDict.keys():
    for date in allStockHistoryDict[stockCode].keys():
        # 取得该票每一天的数据
        data = allStockHistoryDict[stockCode][date]
        # 判断该票当天是否是跳空高开收盘
        if rangeLow < stockUtil.calc_price_change_range(data['pre_close'], data['open']) < rangeHigh:
            if not analysisResult.keys().__contains__(date):
                analysisResult[date] = {}
            if not analysisResult[date].keys().__contains__('jump_high_count'):
                analysisResult[date]['jump_high_count'] = 0
            # 当天跳空高开计数+1
            analysisResult[date]['jump_high_count'] = analysisResult[date]['jump_high_count'] + 1
            # 存放到当天的收盘跳空高开记录中
            if not jumpHighLimitDict.keys().__contains__(date):
                jumpHighLimitDict[date] = {}
            if not jumpHighLimitDict[date].keys().__contains__(stockCode):
                jumpHighLimitDict[date][stockCode] = data


dateList = list(analysisResult.keys())
dateList = sorted(dateList, reverse=False)
codeList = allStockHistoryDict.keys()

preDate = None
preData = {}
# 遍历所有可用交易日期
for date in dateList:
    # 遍历所有的股票代码
    for stockCode in codeList:
        # 取得该票当天的数据
        if allStockHistoryDict[stockCode].keys().__contains__(date):
            data = allStockHistoryDict[stockCode][date]
            # 取得该票前一天的数据，如果没有，则暂时不统计
            if preDate is not None and allStockHistoryDict[stockCode].keys().__contains__(preDate):
                preData = allStockHistoryDict[stockCode][preDate]
                if rangeLow < stockUtil.calc_price_change_range(preData['pre_close'], preData['open']) < rangeHigh:
                    # 判断当天的竞价赚钱效应（判断前一天跳空高开买入第二天开盘的差价）
                    if not analysisResult[date].keys().__contains__('total_jump_high_open_range'):
                        analysisResult[date]['total_jump_high_open_range'] = float(0)
                    curOpen = float(data['open'])
                    preOpen = float(preData['open'])
                    analysisResult[date]['total_jump_high_open_range'] = round(
                        analysisResult[date]['total_jump_high_open_range'] + 100 * (curOpen - preOpen) / preOpen, 2)
                    analysisResult[date]['avg_jump_high_open_range'] = round(
                        analysisResult[date]['total_jump_high_open_range'] / analysisResult[preDate][
                            'jump_high_count'], 2)

                    # 判断当天的高点赚钱效应（判断前一天跳空高开买入第二天高点的差价）
                    if not analysisResult[date].keys().__contains__('total_jump_high_high_range'):
                        analysisResult[date]['total_jump_high_high_range'] = float(0)
                    curHigh = float(data['high'])
                    preOpen = float(preData['open'])
                    analysisResult[date]['total_jump_high_high_range'] = round(
                        analysisResult[date]['total_jump_high_high_range'] + 100 * (curHigh - preOpen) / preOpen, 2)
                    analysisResult[date]['avg_jump_high_high_range'] = round(
                        analysisResult[date]['total_jump_high_high_range'] / analysisResult[preDate][
                            'jump_high_count'], 2)

                    # 判断当天的收盘赚钱效应（判断前一天跳空高开买入第二天收盘的差价）
                    if not analysisResult[date].keys().__contains__('total_jump_high_close_range'):
                        analysisResult[date]['total_jump_high_close_range'] = float(0)
                    curClose = float(data['close'])
                    preOpen = float(preData['open'])
                    analysisResult[date]['total_jump_high_close_range'] = round(
                        analysisResult[date]['total_jump_high_close_range'] + 100 * (curClose - preOpen) / preOpen,
                        2)
                    analysisResult[date]['avg_jump_high_close_range'] = round(
                        analysisResult[date]['total_jump_high_close_range'] / analysisResult[preDate][
                            'jump_high_count'], 2)

                    # 判断当天的竞价亏钱效应（判断前一天跳空高开买入第二天低点的差价）
                    if not analysisResult[date].keys().__contains__('total_jump_high_low_range'):
                        analysisResult[date]['total_jump_high_low_range'] = float(0)
                    curlow = float(data['low'])
                    preOpen = float(preData['open'])
                    analysisResult[date]['total_jump_high_low_range'] = round(
                        analysisResult[date]['total_jump_high_low_range'] + 100 * (curlow - preOpen) / preOpen, 2)
                    analysisResult[date]['avg_jump_high_low_range'] = round(
                        analysisResult[date]['total_jump_high_low_range'] / analysisResult[preDate][
                            'jump_high_count'], 2)

                    # 判断当天的高低点中位数赚钱效应（判断前一天跳空高开买入第二天高低点中值）
                    if not analysisResult[date].keys().__contains__('total_jump_high_low_middle_range'):
                        analysisResult[date]['total_jump_high_low_middle_range'] = float(0)
                    curMiddle = (float(data['high']) + float(data['low']))/float(2)
                    preOpen = float(preData['open'])
                    analysisResult[date]['total_jump_high_low_middle_range'] = round(
                        analysisResult[date]['total_jump_high_low_middle_range'] + 100 * (curMiddle - preOpen) / preOpen, 2)
                    analysisResult[date]['avg_jump_high_low_middle_range'] = round(
                        analysisResult[date]['total_jump_high_low_middle_range'] / analysisResult[preDate][
                            'jump_high_count'], 2)
    preDate = date

print(analysisResult)

######################################################################################
######################################################################################
# 日期列表
x1 = dateList

close_high_jump_count_list = []       # 跳空高开收盘
avg_jump_high_open_range_list = []  # 前一天跳空高开买入第二天开盘的差价
avg_jump_high_close_range_list = [] # 前一天跳空高开买入第二天收盘的差价
avg_jump_high_high_range_list = []  # 前一天跳空高开买入第二天高点的差价
avg_jump_high_low_range_list = []   # 前一天跳空高开买入第二天低点的差价

avg_jump_high_low_middle_range_list = []   # 前一天跳空高开买入第二天高低点的中位数

for date in dateList:
    if analysisResult.keys().__contains__(date):
        # 跳空高开收盘
        if analysisResult[date].keys().__contains__('jump_high_count'):
            close_high_jump_count_list.append(analysisResult[date]['jump_high_count'])
        else:
            close_high_jump_count_list.append(0)

        # 前一天跳空高开买入第二天开盘的差价
        if analysisResult[date].keys().__contains__('avg_jump_high_open_range'):
            avg_jump_high_open_range_list.append(analysisResult[date]['avg_jump_high_open_range'])
        else:
            avg_jump_high_open_range_list.append(0)

        # 前一天跳空高开买入第二天收盘的差价
        if analysisResult[date].keys().__contains__('avg_jump_high_close_range'):
            avg_jump_high_close_range_list.append(analysisResult[date]['avg_jump_high_close_range'])
        else:
            avg_jump_high_close_range_list.append(0)

        # 前一天跳空高开买入第二天高点的差价
        if analysisResult[date].keys().__contains__('avg_jump_high_high_range'):
            avg_jump_high_high_range_list.append(analysisResult[date]['avg_jump_high_high_range'])
        else:
            avg_jump_high_high_range_list.append(0)

        # 前一天跳空高开买入第二天低点的差价
        if analysisResult[date].keys().__contains__('avg_jump_high_low_range'):
            avg_jump_high_low_range_list.append(analysisResult[date]['avg_jump_high_low_range'])
        else:
            avg_jump_high_low_range_list.append(0)


        # 前一天跳空高开买入第二天低点的中位数
        if analysisResult[date].keys().__contains__('avg_jump_high_low_middle_range'):
            avg_jump_high_low_middle_range_list.append(analysisResult[date]['avg_jump_high_low_middle_range'])
        else:
            avg_jump_high_low_middle_range_list.append(0)


#********************************************************************************
# 使用pyecharts生成图表
#********************************************************************************
columns = []
for date in dateList:
    columns.append(date[4:6] + '-' + date[6:8])

bar = (
    Bar(init_opts=opts.InitOpts(width=str(30*dayCount)+'px',height='900px'))
    .add_xaxis(columns)
    .add_yaxis("跳空高开数", close_high_jump_count_list, color="#FF8C00")
    .set_global_opts(title_opts=opts.TitleOpts(title="跳空高开数量分析"), xaxis_opts=opts.AxisOpts(name="日期", axislabel_opts={"rotate": 45}))
)
# bar.render('跳空高开趋势分析.html')


line = (
    Line()
    .add_xaxis(columns)
    .add_yaxis("跳空高开开盘", avg_jump_high_open_range_list)
    .add_yaxis("跳空高开收盘", avg_jump_high_close_range_list)
    .add_yaxis("跳空高开高点", avg_jump_high_high_range_list)
    .add_yaxis("跳空高开低点", avg_jump_high_low_range_list)
    .add_yaxis("跳空高开高低中位数", avg_jump_high_low_middle_range_list)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="跳空高开趋势分析", pos_top="48%"),
        legend_opts=opts.LegendOpts(pos_top="48%"),
        xaxis_opts=opts.AxisOpts(name="日期", axislabel_opts={"rotate": 45}, splitline_opts=opts.SplitLineOpts( is_show=True ), ),
        yaxis_opts=opts.AxisOpts(name="日期", axislabel_opts={"rotate": 45}, splitline_opts=opts.SplitLineOpts(is_show=True), ),
    )
)

filePath = get_home_path() + "\\data\\analysis\\跳空高开趋势分析"+today+".html";

grid = (
    Grid(init_opts=opts.InitOpts(width=str(30*dayCount)+'px',height='900px'))
    .add(bar, grid_opts=opts.GridOpts(pos_bottom="60%"))
    .add(line, grid_opts=opts.GridOpts(pos_top="60%"))
    .render(filePath)
)

