from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import os
import sqlite3
from selenium import webdriver
import time
from urllib import request
from bs4 import BeautifulSoup
import re
import requests
import random
from PyQt5 import QtCore

style = """
        .QPushButton{
        border-style:none;
        border:1px solid #C2CCD8; 
        color:#fff;  
        padding:5px;
        min-height:25px;
        #border-radius:5px;
        selection-color:pink;
        font-size:20px;
        font-weight:800;
        #backgrounE:qlineargradient(spreaE:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #4D4D4D,stop:1 #292929);#渐变色
        }
        # .QPushButton:hover{background-color:white; color: black;}
        # .QPushButton:pressed{background-color:rgb(46, 104, 170); border-style: inset; }
        .QLineEdit{
        font-family:"Courier New";
        font-size:20px;
        }
    """
button_hover = "QPushButton:hover{background-color:rgb(224, 128, 49);}"

##爬取南航首页学术报告信息
response = request.urlopen(r'http://www.nuaa.edu.cn/xsxx1/list.htm')
html = response.read()
soup = BeautifulSoup(html,"html.parser")
title = soup.find_all(name='span',attrs={"class":re.compile(r'column-news-title')})
time = soup.find_all(name='span',attrs={"class":'column-news-date news-date-hide'})
url = soup.find_all(name='a',attrs={"class":re.compile(r'column-news-item item-*')})

##爬取学术南航微信公众号学术报告信息
# try:
#     html1 = requests.get('http://mp.weixin.qq.com/profile?src=3&timestamp=1512978227&ver=1&signature=ZszSVcW79rKywJAn7aJFVbcnWIIbOZACBIkBpdsKRbk4owZ5-qrbmcK5h2aPmm6Q*Y*MB9q6Tk2*jUGr3Z69Ng==').text
#     soup1 = BeautifulSoup(html1, "html.parser")
#     title1 = soup1.find_all(name='script', attrs={"type": 'text/javascript'})
#     infoPara = title1[-2].get_text()
#     info1 = re.findall(r'cover":(.*)content":"","datetime":', infoPara)
#     url1 = re.sub(r'"cover":', r'\n', info1[0])
#     url2 = re.sub(r'","del_flag":1,"digest":', r'\n', url1)
#     resultInfo = re.findall(r'.*"del_flag":1,"digest":"(.*)","fileid":.*', url1, re.M)  ##讲座简介列表
#     imageUrl = re.findall(r'.*"http://(.*)\n.*', url2 + '\n')  ##讲座海报链接列表
#     expendInfo = re.findall(r'.*"title":"(.*)"},"comm_msg_info".*', url1 + ',"fileid":', re.M)  ##额外信息
#     MoreUrl = re.findall(r'"content_url":"(.+?)","copyright_stat"', infoPara)
# except IndexError as e:
#     print("搜狗链接失效！")
# except Exception as e:
#     print('填写搜狗微信平台的验证码！')

# 创建数据库连接
def createConnection():
    # 选择数据库类型，这里为sqlite3数据库
    db = QSqlDatabase.addDatabase("QSQLITE")
    # 创建数据库test0.db,如果存在则打开，否则创建该数据库
    db.setDatabaseName("academicDB.db")
    # 打开数据库
    db.open()

# 创建表
def createTable():
    # 创建QsqlQuery对象，用于执行sql语句
    q = QSqlQuery()
    q.exec_("create table if not exists t1 (题目 nchar(100), 时间 nchar(20), 更多信息 nchar(5000))")
    q.exec_("commit")

class Model(QSqlTableModel):
    def __init__(self, parent):
        QSqlTableModel.__init__(self, parent)
        # 设置要载入的表名
        self.setTable("t1")
        # 这一步应该是执行查询的操作，不太理解
        self.select()
        # 数据更新的策略，详细可以查看Qt文档
        self.setEditStrategy(QSqlTableModel.OnManualSubmit)

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

#表格，用于展示数据库中的数据
class TestWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.resize(1400, 800)  #窗口大小
        self.view = QTableView()
        self.model = Model(self.view)
        self.view.setModel(self.model)
        self.view.setFont(QFont("Courier New", 10)) #设置表格字体
        # 按键布置
        # self.findReport = QPushButton('去听报告')
        # self.delbtn = QPushButton('Delete')
        # self.cz = QPushButton("Modify LoginInfo")
        # # self.Tabclose = QPushButton("Close")
        # self.modify = QPushButton("Modify")
        # 按键样式设置
        # self.findReport.setFont(QFont("Courier New", 10, QFont.Bold))
        # self.findReport.setStyleSheet(button_hover)
        # self.delbtn.setFont(QFont("Courier New", 10, QFont.Bold))
        # self.delbtn.setStyleSheet(button_hover)
        # self.cz.setFont(QFont("Courier New", 10, QFont.Bold))
        # self.cz.setStyleSheet(button_hover)
        # self.Tabclose.setFont(QFont("Courier New", 10, QFont.Bold))
        # self.Tabclose.setStyleSheet(button_hover)
        # self.modify.setFont(QFont("Courier New", 10, QFont.Bold))
        # self.modify.setStyleSheet(button_hover)
        # 表格样式设置
        # self.view.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置单元格不可编辑
        # self.view.setSelectionBehavior(QTableView.SelectRows)  # 选取整行
        self.view.setAlternatingRowColors(True)  # 交替变色
        self.view.setStyleSheet("alternate-background-color: #F5F5F5;")  # 定义交替的色号
        self.view.horizontalHeader().setStyleSheet("::section{Background-color:#2f2f2a;color:#fff;border:#3F3F3F;height:35px}")  # rgb末尾表示透明度0-255
        self.view.horizontalHeader().setFont(QFont("MingLiU", 13, QFont.Bold))
        self.view.horizontalHeader().setSectionResizeMode(0,QHeaderView.Interactive)
        self.view.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.view.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.view.setFrameShape(QFrame.NoFrame)  # 无边框
        # self.view.setColumnWidth(0, 700)
        self.view.setColumnWidth(1, 100)
        # self.view.setColumnWidth(2, 600)
        # 布局设置
        wwg = QWidget(self)
        wl = QHBoxLayout(wwg)
        # layout = QGridLayout()
        # layout.addWidget(self.findReport, 0, 0)
        # layout.addWidget(self.delbtn, 1, 0)
        # layout.addWidget(self.cz, 2, 0)
        # layout.addWidget(self.modify, 3, 0)
        # layout.addWidget(self.Tabclose, 4, 0)
        wl.addWidget(self.view)
        # wl.addLayout(layout)
        # wl.setStretchFactor(layout, 1)
        # wl.setStretchFactor(self.view, 7)
        self.setLayout(wl)
        self.setStyleSheet(style)

    # def paintEvent(self, event):  # 设置背景图片
    #     self.painter = QPainter()
    #     self.painter.begin(self)
    #     self.painter.drawPixmap(self.rect(), QPixmap(resource_path(r"pic\1.png")))
    #     self.painter.end()

#主窗口
class mainw(QMainWindow):
    def __init__(self,parent = None):
        super(mainw, self).__init__(parent)
        self.setWindowIcon(QIcon(resource_path(r'pic\logo.png')))
        self.window1 = TestWidget()
        #进度条
        self.bar = QProgressBar()
        styleBar = """
                        QProgressBar {
                            border: none;
                            color: black;
                            text-align: center;
                            background: rgb(187, 187, 187);
                        }
                        QProgressBar::chunk {
                            border: none;
                            background: #009d00;
                            width:20px;

                        }"""
        self.bar.setStyleSheet(styleBar)
        self.bar.setRange(0,9)

        self.sBar = self.statusBar()  # 创建一个空的状态栏
        self.sBar.addPermanentWidget(self.bar)

        #######################-------菜单栏---------##############
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        helpMenu = menubar.addMenu('Help')

        # 给menu创建一个Action
        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(qApp.quit)
        # 将这个Action添加到fileMenu上
        fileMenu.addAction(exitAction)

        aboutAction = QAction('About', self)
        # aboutAction.setShortcut('Ctrl+M')
        aboutAction.setStatusTip('About this software')
        aboutAction.triggered.connect(self.aboutbtn)
        helpMenu.addAction(aboutAction)

        #######################-------工具栏---------##############
        searchAction = QAction(QIcon(resource_path(r'pic\search.png')), '搜索学术报告', self)
        searchAction.setShortcut('Ctrl+Alt+F')
        searchAction.setStatusTip('搜索学术报告')
        searchAction.triggered.connect(self.loadUrl)
        self.toolbar = self.addToolBar('搜索学术报告')
        self.toolbar.addAction(searchAction)

        clearAction = QAction(QIcon(resource_path(r'pic\clear.png')), '清空', self)
        clearAction.setShortcut('Ctrl+Alt+C')
        clearAction.setStatusTip('清空表格')
        clearAction.triggered.connect(self.clear)
        self.toolbar = self.addToolBar('清空')
        self.toolbar.addAction(clearAction)

        # updateUrlAction = QAction(QIcon(resource_path(r'pic\genxin.ico')), '更新链接', self)
        # updateUrlAction.setShortcut('Ctrl+Alt+U')
        # updateUrlAction.setStatusTip('更新链接')
        # updateUrlAction.triggered.connect(self.updateUrl)
        # self.toolbar = self.addToolBar('更新链接')
        # self.toolbar.addAction(updateUrlAction)

        fileMenu.addAction(searchAction)
        fileMenu.addAction(clearAction)
        # fileMenu.addAction(updateUrlAction)

        self.setWindowTitle('南航学术报告搜索平台')
        # self.setGeometry(300, 300, 450, 0)

        ##使表格这个QWidget成为QMainWindow的一部分
        self.mainFormLayout = QVBoxLayout(self.window1)
        self.window1.setLayout(self.mainFormLayout)
        self.setCentralWidget(self.window1)


    def clear(self):
        q = QSqlQuery()
        q.exec_("delete from t1")
        q.exec_("commit")
        self.window1.model.submitAll()

    def aboutbtn(self):
        QMessageBox.about(self, u'About', u'Account Manager (Version 1.0)\n\nThis software is used to record your account and password. The \'admin\' row represents login information, it cannot be delete!\n\n\n\nwcb All Rights Reserved')
    # def updateUrl(self):
    #     path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver\chromedriver.exe"
    #     driver = webdriver.Chrome(executable_path=path)
    #     try:
    #         driver.get('http://weixin.sogou.com/')
    #         driver.find_element_by_id('query').clear()
    #         driver.find_element_by_id('query').send_keys('南航学术交流')
    #         # time.sleep(2)
    #         driver.find_element_by_class_name('swz2').click()
    #         xsUrl = driver.current_url
    #         xsResponse = request.urlopen(xsUrl)
    #         xsHtml = xsResponse.read()
    #         soup = BeautifulSoup(xsHtml, "html.parser")
    #         table = soup.find_all(name='a', attrs={"uigs": 'account_name_0'})
    #         current_XsUrl = table[0].get('href')
    #         # time.sleep(1)
    #         driver.quit()
    #     except Exception as e:
    #         current_XsUrl = 'failed'
    #     f = open(resource_path(r'CurrentUrl.txt'), "w")
    #     f.write(current_XsUrl)
    #     f.close()
    #     QMessageBox.information(self, u'成功','更新成功！')
    def loadUrl(self):
        fUrl = open(resource_path(r'CurrentUrl.txt'))
        self.Url = fUrl.read()
        self.loadAcademic()
    def loadAcademic(self):
        for i in range(0, 10):
            ##官网
            response = request.urlopen('http://www.nuaa.edu.cn' + url[i].get('href'))
            html = response.read()
            soup = BeautifulSoup(html, "html.parser")
            info1 = soup.find_all('meta')[-1].get('content')
            info2 = ''
            for jj in soup.find_all(name='span', attrs={"style": re.compile('.*')}):
                info2 = info2 + jj.get_text()
            Title = title[i].text
            # Info = ''
            Info = info1+info2
            try:
                jzDate = re.findall(r"(\d{1,2}月\d{1,2}日)", Info)[0]
            except Exception as e:
                jzDate = '无'
            try:
                jzTime = re.findall(r"(\d{2}:\d{2})", Info)[0]
            except Exception as e:
                jzTime = '无'
            try:
                place = re.findall(r".*地\s|点.*", Info)[0]
            except Exception as e:
                place = '无'
            q = QSqlQuery()
            q.exec_(u"insert into t1 values('%s','%s','%s')" % (Title, jzDate+jzTime, info1))
            # q.exec_(u"insert into t1 values('%s','%s','%s')" % (Title, '', Info))
            q.exec_("commit")
            self.window1.model.submitAll()
            self.bar.setValue(i)########进度条
        self.bar.reset()
if __name__ == "__main__":
    a = QApplication(sys.argv)
    createConnection()
    createTable()
    w = mainw()
    w.resize(1400, 800)
    w.show()
    sys.exit(a.exec_())
