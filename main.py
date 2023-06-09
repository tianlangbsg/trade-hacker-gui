# ///////////////////////////////////////////////////////////////
import random
import sys
import os
import platform

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
import threading
import time

from PySide6.QtCore import Signal, QTimer
from PySide6.QtGui import QStandardItem, QStandardItemModel

from modules import *
from modules.core import stockHacker
from modules.core.common import common_variables
import modules.core.utils.logUtil as log
from modules.core.simulationTrader.service.tradeRecordService import getTodayRecords
from widgets import *
os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        # 设置到全局变量中
        common_variables.ui_widgets = widgets

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "Trade Hacker"
        description = "Trade Hacker"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_trade.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)

        # HOME
        widgets.btn_start.clicked.connect(self.buttonClick)
        widgets.btn_stop.clicked.connect(self.buttonClick)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        # themeFile = "themes\py_dracula_light.qss"
        themeFile = "themes\py_dracula_dark.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))


        # web browser test
        # from PySide6.QtWebEngineWidgets import QWebEngineView
        # self.widget_browser1 = QWebEngineView()
        # self.widget_browser1.load(QUrl("https://baidu.com"))
        # self.widget_browser1.setObjectName(u"widget_browser1")
        # self.widget_browser1.setMinimumSize(QSize(500, 800))
        # web browser test

    refreshStatus = False
    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_trade":
            widgets.stackedWidget.setCurrentWidget(widgets.trade) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

            # 判断是否已经初始化过一次
            if self.refreshStatus is False:
                # 刷新备选池列表(top N)
                self.refresh_tbv_alternative()
                # 刷新当日交易记录
                self.refresh_tbv_trade_record()
                # 刷新账户状态
                self.refresh_account_status()
                # 刷新持仓状态
                # self.refresh_position()

                self.refreshStatus = True

        if btnName == "btn_save":
            print("Save BTN clicked!")

        # PAGE HOME BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////
        if btnName == "btn_start":
            widgets.btn_start.setEnabled(False)
            widgets.btn_stop.setEnabled(True)

            common_variables.homeThreadStatus = True

            common_variables.homeThread = threading.Thread(target=stockHacker.start)
            common_variables.homeThread.start()

        if btnName == "btn_stop":
            widgets.btn_start.setEnabled(True)
            widgets.btn_stop.setEnabled(False)
            common_variables.homeThreadStatus = False
            log.info("主线程关闭")

        # PRINT BTN NAME
        log.info(f'Button "{btnName}" pressed!')

    def start_running(self):
        try:
            # stockHacker.start()
            import modules.core.utils.logUtil as log
            log.info("系统初始化完成")
        except Exception as e:
            widgets.txt_info.setText('Error:' + e.__str__())

    def stop_running(self):
        try:
            stockHacker.stop()
        except Exception as e:
            widgets.txt_info.setText('Error:' + e.__str__())

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

    # DATA REFRESH EVENTS
    # ///////////////////////////////////////////////////////////////
    # 刷新备选池
    refresh_tbv_alternative_signal = Signal()
    refresh_tbv_alternative_timer = QTimer()
    def refresh_tbv_alternative(self):
        try:
            self.alternative_model = QStandardItemModel()
            self.ui.tbv_alternative.setModel(self.alternative_model)

            self.refresh_tbv_alternative_timer.timeout.connect(self.on_tbv_alternative_timeout)
            # 定义刷新间隔
            self.refresh_tbv_alternative_timer.start(2000)
            # 关联刷新函数
            self.refresh_tbv_alternative_signal.connect(self.refresh_tbv_alternative_data)
        except Exception as ex:
            log.error('UI 备选池刷新错误:' + ex.__str__())

    def on_tbv_alternative_timeout(self):
        self.refresh_tbv_alternative_signal.emit()

    def refresh_tbv_alternative_data(self):
        try:
            self.alternative_model.clear()
            self.alternative_model = QStandardItemModel(0, 0, self)

            self.alternative_model.setHorizontalHeaderItem(0, QStandardItem("代码"))
            self.alternative_model.setHorizontalHeaderItem(1, QStandardItem("名字"))
            self.alternative_model.setHorizontalHeaderItem(2, QStandardItem("涨幅"))
            self.alternative_model.setHorizontalHeaderItem(3, QStandardItem("成交量"))
            self.alternative_model.setHorizontalHeaderItem(4, QStandardItem("开盘"))
            self.alternative_model.setHorizontalHeaderItem(5, QStandardItem("现价"))
            self.alternative_model.setHorizontalHeaderItem(6, QStandardItem("卖一量"))
            self.alternative_model.setHorizontalHeaderItem(7, QStandardItem("卖一金额（万）"))
            self.alternative_model.setHorizontalHeaderItem(8, QStandardItem("卖二量"))
            self.alternative_model.setHorizontalHeaderItem(9, QStandardItem("卖二金额（万）"))
            self.alternative_model.setHorizontalHeaderItem(10, QStandardItem("卖三量"))
            self.alternative_model.setHorizontalHeaderItem(11, QStandardItem("卖三金额（万）"))

            for stockCode in common_variables.stockRank100Dict.keys():
                self.alternative_model.appendRow([QStandardItem(common_variables.stockRank100Dict[stockCode]['code']),
                                      QStandardItem(common_variables.stockRank100Dict[stockCode]['name']),
                                      QStandardItem(str(common_variables.stockRank100Dict[stockCode]['change_range'])),
                                      QStandardItem(str(common_variables.stockRank100Dict[stockCode]['open'])),
                                      QStandardItem(str(common_variables.stockRank100Dict[stockCode]['now'])),
                                      QStandardItem(str(common_variables.stockRank100Dict[stockCode]['volume'])),
                                      QStandardItem(str(common_variables.stockRank100Dict[stockCode]['ask1_volume'])),
                                      QStandardItem(str(int((float(common_variables.stockRank100Dict[stockCode]['ask1_volume'])*float(common_variables.stockRank100Dict[stockCode]['ask1']))/10000))),
                                      QStandardItem(str(common_variables.stockRank100Dict[stockCode]['ask2_volume'])),
                                      QStandardItem(str(int((float(common_variables.stockRank100Dict[stockCode]['ask2_volume'])*float(common_variables.stockRank100Dict[stockCode]['ask2']))/10000))),
                                      QStandardItem(str(common_variables.stockRank100Dict[stockCode]['ask3_volume'])),
                                      QStandardItem(str(int((float(common_variables.stockRank100Dict[stockCode]['ask3_volume']) * float(common_variables.stockRank100Dict[stockCode]['ask3'])) / 10000))),
                                      ])

            # 将数据模型绑定到QTableView
            self.ui.tbv_alternative.setModel(self.alternative_model)
            # 设置列宽
            for i in range(0,12):
                self.ui.tbv_alternative.setColumnWidth(i,70)
        except Exception as ex:
            log.error('UI 备选池刷新错误:' + ex.__str__())



    # ///////////////////////////////////////////////////////////////
    # 刷新交易记录
    refresh_tbv_trade_record_signal = Signal()
    refresh_tbv_trade_record_timer = QTimer()

    def refresh_tbv_trade_record(self):
        try:
            self.records_model = QStandardItemModel()
            self.ui.tbv_trade_record.setModel(self.records_model)

            self.refresh_tbv_trade_record_timer.timeout.connect(self.on_tbv_trade_record_timeout)
            # 定义刷新间隔5秒
            self.refresh_tbv_trade_record_timer.start(3000)
            # 关联刷新函数
            self.refresh_tbv_trade_record_signal.connect(self.refresh_tbv_trade_record_data)
        except Exception as ex:
            log.error('UI 备选池刷新错误:' + ex.__str__())

    def on_tbv_trade_record_timeout(self):
        self.refresh_tbv_trade_record_signal.emit()

    def refresh_tbv_trade_record_data(self):
        try:
            self.records_model.clear()
            self.records_model = QStandardItemModel(0, 0, self)

            self.records_model.setHorizontalHeaderItem(0, QStandardItem("代码"))
            self.records_model.setHorizontalHeaderItem(1, QStandardItem("名字"))
            self.records_model.setHorizontalHeaderItem(2, QStandardItem("详情"))
            self.records_model.setHorizontalHeaderItem(3, QStandardItem("成交价格"))
            self.records_model.setHorizontalHeaderItem(4, QStandardItem("成交数量"))
            self.records_model.setHorizontalHeaderItem(5, QStandardItem("成交时间"))
            self.records_model.setHorizontalHeaderItem(6, QStandardItem("交易类型"))
            self.records_model.setHorizontalHeaderItem(7, QStandardItem("成交金额"))

            # 从数据库取得当天交易记录
            tradeRecordDict = getTodayRecords()

            for key in tradeRecordDict.keys():
                self.records_model.appendRow([QStandardItem(tradeRecordDict[key]['stock_code']),
                                      QStandardItem(tradeRecordDict[key]['stock_name']),
                                      QStandardItem(tradeRecordDict[key]['detail']),
                                      QStandardItem(tradeRecordDict[key]['trade_price']),
                                      QStandardItem(tradeRecordDict[key]['trade_amount']),
                                      QStandardItem(str(tradeRecordDict[key]['timestamp'])[11: 19]),
                                      QStandardItem(tradeRecordDict[key]['trade_type']),
                                      QStandardItem(str(tradeRecordDict[key]['money'])),
                                      ])

            # 将数据模型绑定到QTableView
            self.ui.tbv_trade_record.setModel(self.records_model)
            # 设置列宽
            for i in range(0,8):
                self.ui.tbv_trade_record.setColumnWidth(i,70)

        except Exception as ex:
            log.error('UI 交易记录刷新错误:' + ex.__str__())



    # ///////////////////////////////////////////////////////////////

    # ///////////////////////////////////////////////////////////////
    # 刷新账户状态
    refresh_account_status_signal = Signal()
    refresh_account_status_timer = QTimer()

    def refresh_account_status(self):
        try:
            self.refresh_account_status_timer.timeout.connect(self.on_account_status_timeout)
            # 定义刷新间隔
            self.refresh_account_status_timer.start(5000)
            # 关联刷新函数
            self.refresh_account_status_signal.connect(self.refresh_account_status_data)
        except Exception as ex:
            log.error('UI 备选池刷新错误:' + ex.__str__())

    def on_account_status_timeout(self):
        self.refresh_account_status_signal.emit()

    def refresh_account_status_data(self):
        try:
            self.ui.lbl_balance_value.setText(str(random.randint(1,999999999)))
            self.ui.lbl_available_value.setText(str(random.randint(1,999999999)))
            self.ui.lbl_market_value_value.setText(str(random.randint(1,999999999)))
            self.ui.lbl_profit_value.setText(str(random.randint(1,999999999)))
            self.ui.lbl_today_profit_value.setText(str(random.randint(1,999999999)))
            self.ui.lbl_today_profit_rate.setText(str(random.randint(1,999999999)))

        except Exception as ex:
            log.error('UI 账户状态刷新错误:' + ex.__str__())

    # ///////////////////////////////////////////////////////////////

    # ///////////////////////////////////////////////////////////////
    # 刷新账户状态
    # refresh_position_signal = Signal()
    # refresh_position_timer = QTimer()
    #
    # def refresh_position(self):
    #     try:
    #         self.refresh_position_timer.timeout.connect(self.on_position_timeout)
    #         # 定义刷新间隔
    #         self.refresh_position_timer.start(5000)
    #         # 关联刷新函数
    #         self.refresh_position_signal.connect(self.refresh_position_data)
    #     except Exception as ex:
    #         log.error('UI 备选池刷新错误:' + ex.__str__())
    #
    # def on_position_timeout(self):
    #     self.refresh_position_signal.emit()
    #
    # def refresh_position_data(self):
    #     try:
    #         self.position_model.clear()
    #         self.position_model = QStandardItemModel(0, 0, self)
    #
    #         self.position_model.setHorizontalHeaderItem(0, QStandardItem("代码"))
    #         self.position_model.setHorizontalHeaderItem(1, QStandardItem("名字"))
    #         self.position_model.setHorizontalHeaderItem(2, QStandardItem("市值"))
    #         self.position_model.setHorizontalHeaderItem(3, QStandardItem("盈亏"))
    #         self.position_model.setHorizontalHeaderItem(4, QStandardItem("盈亏率"))
    #         self.position_model.setHorizontalHeaderItem(5, QStandardItem("当日盈亏"))
    #         self.position_model.setHorizontalHeaderItem(6, QStandardItem("当日盈亏率"))
    #         self.position_model.setHorizontalHeaderItem(7, QStandardItem("持仓数量"))
    #         self.position_model.setHorizontalHeaderItem(8, QStandardItem("可卖数量"))
    #         self.position_model.setHorizontalHeaderItem(9, QStandardItem("成本"))
    #         self.position_model.setHorizontalHeaderItem(10, QStandardItem("现价"))
    #
    #         # 从数据库取得当天交易记录
    #         tradeRecordDict = getTodayRecords()
    #
    #         for key in tradeRecordDict.keys():
    #             self.records_model.appendRow([QStandardItem(tradeRecordDict[key]['stock_code']),
    #                                   QStandardItem(tradeRecordDict[key]['stock_name']),
    #                                   QStandardItem(tradeRecordDict[key]['detail']),
    #                                   QStandardItem(tradeRecordDict[key]['trade_price']),
    #                                   QStandardItem(tradeRecordDict[key]['trade_amount']),
    #                                   QStandardItem(str(tradeRecordDict[key]['timestamp'])[11: 19]),
    #                                   QStandardItem(tradeRecordDict[key]['trade_type']),
    #                                   QStandardItem(str(tradeRecordDict[key]['money'])),
    #                                   ])
    #
    #         # 将数据模型绑定到QTableView
    #         self.ui.tbv_trade_record.setModel(self.records_model)
    #         # 设置列宽
    #         for i in range(0,1):
    #             self.ui.tbv_trade_record.setColumnWidth(i,80)
    #
    #     except Exception as ex:
    #         log.error('UI 持仓状态刷新错误:' + ex.__str__())

    # ///////////////////////////////////////////////////////////////

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
