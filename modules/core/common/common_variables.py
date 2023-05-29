# UI控件
global ui_widgets  # 全局ui_main控件

# 线程
# 首页子线程
global homeThread
# 后台子线程
global refreshRealThread  # 实时行情刷新
global refreshTop100Thread  # 涨幅前100实时行情刷新
global selectTargetThread  # 选股逻辑
# ui后台子线程
global refreshUITopThread  # ui涨幅前n个实时行情刷新

refreshRealThread = None
refreshTop100Thread = None
selectTargetThread = None
refreshUITopThread = None

# 股票数据list
global rawStockCodeList  # 原始不带前缀
global stockCodeList  # 带前缀
global stockHistoryList  # 股票历史数据
global stockRankList  # 股票涨跌幅排行
global stockRank100List  # 股票涨幅排行前100
# 全股票数据集合
global stockHistoryDict  # 股票上个交易日信息
global allStockHistoryDict  # 过去指定时间内全部股票信息
global stockRealDict  # 股票实时信息
global stockRankDict  # 股票涨跌幅排行
global stockRank100Dict  # 股票涨幅排行前100
global stockTargetDict  # 目标要操作的股票信息（含5档）
global candidateList  # 候选股票

# 股票数据list
rawStockCodeList = []  # 原始不带前缀
stockCodeList = []  # 带前缀
stockHistoryList = []  # 股票历史数据
stockRankList = []  # 股票涨跌幅排行
stockRank100List = []  # 股票涨幅排行前100

# 全股票数据集合
stockHistoryDict = {}  # 股票上个交易日信息
allStockHistoryDict = {}  # 过去指定时间内全部股票信息
stockRealDict = {}  # 股票实时信息
stockRankDict = {}  # 股票涨跌幅排行
stockRank100Dict = {}  # 股票涨幅排行前100
stockTargetDict = {}  # 目标要操作的股票信息（含5档）
candidateList = {}  # 候选股票
