# ///////////////////////////////////////////////////////////////
import sys
import os
import platform

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
import threading
import time

from PySide6.QtCore import Signal
from PySide6.QtGui import QStandardItem

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

            # 刷新备选池列表(top N)
            self.refresh_tbv_alternative()
            # 刷新当日交易记录
            self.refresh_tbv_trade_record()

        if btnName == "btn_save":
            print("Save BTN clicked!")

        # PAGE HOME BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////
        if btnName == "btn_start":
            widgets.btn_start.setEnabled(False)
            widgets.btn_stop.setEnabled(True)

            common_variables.homeThread = threading.Thread(target=stockHacker.start)
            common_variables.homeThread.start()


        if btnName == "btn_stop":
            widgets.btn_start.setEnabled(True)
            widgets.btn_stop.setEnabled(False)
            if common_variables.homeThread is None:
                log.error("HomeThread没有执行")
            else:
                common_variables.homeThread.stop()


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
        self.alternative_model = QStandardItemModel()
        self.ui.tbv_alternative.setModel(self.alternative_model)

        self.refresh_tbv_alternative_timer.timeout.connect(self.on_tbv_alternative_timeout)
        # 定义刷新间隔1秒
        self.refresh_tbv_alternative_timer.start(5000)
        # 关联刷新函数
        self.refresh_tbv_alternative_signal.connect(self.refresh_tbv_alternative_data)

    def on_tbv_alternative_timeout(self):
        self.refresh_tbv_alternative_signal.emit()

    def refresh_tbv_alternative_data(self):
        try:
            self.alternative_model.clear()
            try:
                self.alternative_model = QStandardItemModel(0, 0, self)

                self.alternative_model.setHorizontalHeaderItem(0, QStandardItem("代码"))
                self.alternative_model.setHorizontalHeaderItem(1, QStandardItem("名字"))
                self.alternative_model.setHorizontalHeaderItem(2, QStandardItem("开盘"))
                self.alternative_model.setHorizontalHeaderItem(3, QStandardItem("现价"))
                self.alternative_model.setHorizontalHeaderItem(4, QStandardItem("涨幅"))
                self.alternative_model.setHorizontalHeaderItem(5, QStandardItem("成交量"))
                self.alternative_model.setHorizontalHeaderItem(6, QStandardItem("涨停价"))
                self.alternative_model.setHorizontalHeaderItem(7, QStandardItem("跌停价"))

                for stockCode in common_variables.stockRankList[0:60]:
                    # item = QStandardItem('({}, {})'.format(common_variables.stockRank100Dict[stockCode]['limit_high'], column))
                    self.alternative_model.appendRow([QStandardItem(common_variables.stockRank100Dict[stockCode[0]]['code']),
                                          QStandardItem(common_variables.stockRank100Dict[stockCode[0]]['name']),
                                          QStandardItem(str(common_variables.stockRank100Dict[stockCode[0]]['open'])),
                                          QStandardItem(str(common_variables.stockRank100Dict[stockCode[0]]['now'])),
                                          QStandardItem(
                                              str(common_variables.stockRank100Dict[stockCode[0]]['change_range'])),
                                          QStandardItem(str(common_variables.stockRank100Dict[stockCode[0]]['volume'])),
                                          QStandardItem(str(common_variables.stockRank100Dict[stockCode[0]]['涨停价'])),
                                          QStandardItem(str(common_variables.stockRank100Dict[stockCode[0]]['跌停价'])),
                                          ])

                # 将数据模型绑定到QTableView
                self.ui.tbv_alternative.setModel(self.alternative_model)
            except Exception as ex:
                log.error('UI 备选池刷新错误:' + ex.__str__())
        except Exception as ex:
            log.error('UI 备选池刷新错误:' + ex.__str__())


    # ///////////////////////////////////////////////////////////////
    # 刷新交易记录
    refresh_tbv_trade_record_signal = Signal()
    refresh_tbv_trade_record_timer = QTimer()

    def refresh_tbv_trade_record(self):
        self.records_model = QStandardItemModel()
        self.ui.tbv_trade_record.setModel(self.records_model)

        self.refresh_tbv_trade_record_timer.timeout.connect(self.on_tbv_trade_record_timeout)
        # 定义刷新间隔5秒
        self.refresh_tbv_trade_record_timer.start(5000)
        # 关联刷新函数
        self.refresh_tbv_trade_record_signal.connect(self.refresh_tbv_trade_record_data)

    def on_tbv_trade_record_timeout(self):
        self.refresh_tbv_trade_record_signal.emit()

    def refresh_tbv_trade_record_data(self):
        try:
            self.records_model.clear()
            try:
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
                                          QStandardItem(str(tradeRecordDict[key]['timestamp'])),
                                          QStandardItem(tradeRecordDict[key]['trade_type']),
                                          QStandardItem(str(tradeRecordDict[key]['money'])),
                                          ])

                # 将数据模型绑定到QTableView
                self.ui.tbv_trade_record.setModel(self.records_model)
            except Exception as ex:
                log.error('UI 交易记录刷新错误:' + ex.__str__())
        except Exception as ex:
            log.error('UI 交易记录刷新错误:' + ex.__str__())


    # ///////////////////////////////////////////////////////////////

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
