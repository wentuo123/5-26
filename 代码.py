import sys
import pymysql
import re   # 正则表达式
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget, QTableWidget, \
    QTableWidgetItem, QMainWindow, QHeaderView
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QFont


# 注册界面
# 用户的基本注册信息
class user_register():
    def __init__(self, account, password):
        self.account = account
        self.password = password

class Ui_register(object):
    def register_ui(self, Register_Window):
        Register_Window.setObjectName("Register_Window")
        Register_Window.setFixedSize(372, 189)
        Register_Window.setWindowIcon(QIcon("780.ico"))

        # 连接数据库
        self.db = pymysql.connect(
            host="localhost",
            user="root",
            password="123456",
            database="Select_Ticket_System",
        )
        # 获取操作数据库的游标
        self.cursor = self.db.cursor()

        self.pushButton = QtWidgets.QPushButton(Register_Window)
        self.pushButton.setGeometry(QtCore.QRect(10, 130, 351, 51))
        self.pushButton.setStyleSheet("font: 20pt \"楷体\";\n""background-color: rgb(85, 170, 255);")
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(Register_Window)
        self.label_2.setGeometry(QtCore.QRect(9, 79, 84, 27))
        self.label_2.setStyleSheet("font: 16pt \"楷体\";")
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(Register_Window)
        self.label.setGeometry(QtCore.QRect(10, 20, 84, 27))
        self.label.setStyleSheet("font: 16pt \"楷体\";")
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Register_Window)
        self.lineEdit.setPlaceholderText("请输入账号")
        self.lineEdit.setGeometry(QtCore.QRect(101, 21, 250, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Register_Window)
        self.lineEdit_2.setGeometry(QtCore.QRect(100, 80, 250, 30))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setPlaceholderText("请输入密码")

        self.retranslateUi(Register_Window)
        QtCore.QMetaObject.connectSlotsByName(Register_Window)


    def retranslateUi(self, Register_Window):
        _translate = QtCore.QCoreApplication.translate
        Register_Window.setWindowTitle(_translate("Register_Window", "cmz_注册界面"))
        self.pushButton.setText(_translate("Register_Window", "注册"))
        self.label_2.setText(_translate("Register_Window", "密码："))
        self.label.setText(_translate("Register_Window", "账号："))
        self.pushButton.clicked.connect(self.add_user)

    def add_user(self):
        # 获取输入的账号，密码
        get_account = self.lineEdit.text()
        get_password = self.lineEdit_2.text()

        # 判断插入的数据是否完整
        if not get_account or not get_password:
            box_1 = QMessageBox()
            box_1.setWindowTitle("提示")
            box_1.setText("请填入完整的信息！")
            box_1.setStandardButtons(QMessageBox.Yes)
            box_1.exec()
            self.clear_user_information()
            return


        # 检查是否重复
        # 将文本中读取到的数据按整行去除掉单引号，逗号，括号和换行符
        with open('result.txt', 'r') as f:
            data = f.readlines()  # 读取整个文件内容并按行分割成列表
        new_data = []  # 声明一个新的列表，用于存储处理后的数据
        for line in data:
            new_line_1 = re.sub(r"['()\n]", "", line)  # 使用正则表达式替换对应的符号
            new_line_2 = new_line_1.split(',')[0]
            new_data.append(new_line_2)  # 将处理后的行添加到新的列表中
            # new_data是注册用户的  用户名列表
        for check in new_data:
            if check == get_account:
                box_2 = QMessageBox()
                box_2.setWindowTitle("提示")
                box_2.setText("用户名已存在！")
                box_2.setStandardButtons(QMessageBox.Yes)
                box_2.exec()
                self.clear_user_information()
                return

        # 得到用户的注册信息  包括 账号和密码
        # 插入数据到数据库
        if get_account != "" and get_password != "":
            sql = "INSERT INTO user (account, password) VALUES (%s, %s)"
            val = (get_account, get_password)
            self.cursor.execute(sql, val)
            self.db.commit()

        # 读取数据并写入文本文件
        select_sql = "select * from user"
        self.cursor.execute(select_sql)
        with open('data.txt', 'w') as f:
            for row in self.cursor:
                f.write(str(row) + '\n')
                f.flush()  # 刷新文件缓冲区
        # 去除掉文本中相同的数据
        with open('data.txt', 'r') as f:
            data = set()
            for line in f:
                data.add(line.strip())  # 去除字符串两端的空格，并添加到集合中
        with open('result.txt', 'w') as f:   # 这是最终的注册成功的数据
            for item in data:
                f.write(item + '\n')  # 将集合中的每一项写入文件

        print(new_data)
        box_3 = QMessageBox()
        box_3.setWindowTitle("提示")
        box_3.setText("注册成功！")
        box_3.setStandardButtons(QMessageBox.Yes)
        box_3.exec()
        register_interface.close()
        self.clear_user_information()
        return

    def clear_user_information(self):
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')

    def register_open(self):
        register_1 = QWidget()
        register_1.show()


# 购票界面
class Ui_buy_ticket(object):
    def buy_ticket_ui(self, widget):
        widget.setObjectName("c")
        widget.setFixedSize(1050, 813)

        widget.setWindowIcon(QIcon("780.ico"))
        self.gridLayoutWidget = QtWidgets.QWidget(widget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1053, 812))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_13 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_13.setStyleSheet("font: 11pt \"楷体\";")
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 4, 1, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_3.setStyleSheet("background-color: rgb(255, 101, 104);\n""font: 12pt \"黑体\";")
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 2, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setStyleSheet("background-color: rgb(255, 101, 104);\n""font: 12pt \"黑体\";")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("购票界面图片/3.jpg"))
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_14.setStyleSheet("font: 11pt \"楷体\";")
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 4, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_9.setStyleSheet("font: 11pt \"楷体\";")
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 1, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_12.setStyleSheet("font: 11pt \"楷体\";")
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 4, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_16.setEnabled(True)
        self.label_16.setText("")
        self.label_16.setPixmap(QtGui.QPixmap("购票界面图片/6.jpg"))
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("购票界面图片/1.jpg"))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_11.setText("")
        self.label_11.setPixmap(QtGui.QPixmap("购票界面图片/5.jpg"))
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 3, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("购票界面图片/8.jpg"))
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 3, 3, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_4.setStyleSheet("background-color: rgb(255, 101, 104);\n""font: 12pt \"黑体\";")
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 2, 3, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_8.setStyleSheet("font: 11pt \"楷体\";")
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 1, 2, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_10.setStyleSheet("font: 11pt \"楷体\";")
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_15.setText("")
        self.label_15.setPixmap(QtGui.QPixmap("购票界面图片/7.jpg"))
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 3, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_7.setStyleSheet("font: 11pt \"楷体\";")
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 1, 3, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 101, 104);\n""font: 12pt \"黑体\";")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 2, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setStyleSheet("font: 11pt \"楷体\";")
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("购票界面图片/2.jpg"))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("购票界面图片/4.jpg"))
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 3, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_5.setStyleSheet("background-color: rgb(255, 101, 104);\n""font: 12pt \"黑体\";")
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 5, 0, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_6.setStyleSheet("background-color: rgb(255, 101, 104);\n""font: 12pt \"黑体\";")
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 5, 1, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_7.setStyleSheet("background-color: rgb(255, 101, 104);\n""font: 12pt \"黑体\";")
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout.addWidget(self.pushButton_7, 5, 2, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_8.setStyleSheet("background-color: rgb(255, 101, 104);\n""font: 12pt \"黑体\";")
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout.addWidget(self.pushButton_8, 5, 3, 1, 1)

        self.retranslateUi(widget)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "cmz_购票界面"))
        self.label_13.setText(_translate("widget", "喜羊羊与灰太狼之飞马奇遇记"))
        self.pushButton_3.setText(_translate("widget", "购票"))
        self.pushButton.setText(_translate("widget", "购票"))
        self.label_14.setText(_translate("widget", "喜羊羊与灰太狼之羊年喜羊羊"))
        self.label_9.setText(_translate("widget", "喜羊羊与灰太狼之虎虎生威"))
        self.label_12.setText(_translate("widget", "喜羊羊与灰太狼之开心过蛇年"))
        self.pushButton_4.setText(_translate("widget", "购票"))
        self.label_8.setText(_translate("widget", "喜羊羊与灰太狼之兔年顶呱呱"))
        self.label_10.setText(_translate("widget", "喜羊羊与灰太狼之牛气冲天"))
        self.label_7.setText(_translate("widget", "喜羊羊与灰太狼之开心闯龙门"))
        self.pushButton_2.setText(_translate("widget", "购票"))
        self.label_5.setText(_translate("widget", "喜羊羊与灰太狼之框出未来"))
        self.pushButton_5.setText(_translate("widget", "购票"))
        self.pushButton_6.setText(_translate("widget", "购票"))
        self.pushButton_7.setText(_translate("widget", "购票"))
        self.pushButton_8.setText(_translate("widget", "购票"))

        self.pushButton.clicked.connect(lambda :select_seat_interface.show())
        self.pushButton_2.clicked.connect(lambda :select_seat_interface_2.show())
        self.pushButton_3.clicked.connect(lambda :select_seat_interface_3.show())
        self.pushButton_4.clicked.connect(lambda :select_seat_interface_4.show())
        self.pushButton_5.clicked.connect(lambda :select_seat_interface_5.show())
        self.pushButton_6.clicked.connect(lambda :select_seat_interface_6.show())
        self.pushButton_7.clicked.connect(lambda :select_seat_interface_7.show())
        self.pushButton_8.clicked.connect(lambda :select_seat_interface_8.show())


        # 判断电影名字
        self.label_name = None

    def judge_movie_name(self):
        sender = buy_ticket_interface.sender()
        if sender == self.pushButton:
            self.label_name = self.label_10.text()
        elif sender == self.pushButton_2:
            self.label_name = self.label_9.text()
        elif sender == self.pushButton_3:
            self.label_name = self.label_8.text()
        elif sender == self.pushButton_4:
            self.label_name = self.label_7.text()
        elif sender == self.pushButton_5:
            self.label_name = self.label_12.text()
        elif sender == self.pushButton_6:
            self.label_name = self.label_13.text()
        elif sender == self.pushButton_7:
            self.label_name = self.label_14.text()
        elif sender == self.pushButton_8:
            self.label_name = self.label_5.text()

# 选座界面
class Ui_select_seat(object):
    def select_seat_ui(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(334, 337)
        Form.setStyleSheet("")
        Form.setWindowIcon(QIcon("780.ico"))
        self.label_13 = QtWidgets.QLabel(Form)
        self.label_13.setGeometry(QtCore.QRect(110, 10, 121, 31))
        self.label_13.setStyleSheet("font: 18pt \"楷体\";\n""background-color: rgb(255, 255, 255);")
        self.label_13.setObjectName("label_13")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(30, 290, 141, 41))
        self.pushButton.setStyleSheet("font: 18pt \"楷体\";\n""background-color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 50, 315, 233))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);\n""font: 12pt \"黑体\";")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setStyleSheet("background-color: rgb(255, 255, 255);\n""font: 12pt \"黑体\";")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setStyleSheet("background-color: rgb(255, 255, 255);\n""font: 12pt \"黑体\";")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setStyleSheet("background-color: rgb(255, 255, 255);\n""font: 12pt \"黑体\";")
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 4, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setStyleSheet("background-color: rgb(255, 255, 255);\n""font: 12pt \"黑体\";")
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 5, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        self.label_6.setStyleSheet("background-color: rgb(255, 255, 255);\n""font: 12pt \"黑体\";")
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 6, 1, 2)
        self.label_7 = QtWidgets.QLabel(self.layoutWidget)
        self.label_7.setStyleSheet("background-color: rgb(255, 255, 255);\n""font: 12pt \"黑体\";")
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 1)
        self.pushButton_1 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_1.setStyleSheet("background-color: rgb(255, 255, 255);\n""font: 12pt \"楷体\";")
        self.pushButton_1.setText("")
        self.pushButton_1.setObjectName("pushButton_1")
        self.gridLayout.addWidget(self.pushButton_1, 1, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 2, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 1, 3, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_4.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_4.setText("")
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 1, 4, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_5.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_5.setText("")
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 1, 5, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.layoutWidget)
        self.label_8.setStyleSheet("background-color: rgb(255, 255, 255);\n""font: 12pt \"黑体\";")
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_7.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_7.setText("")
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout.addWidget(self.pushButton_7, 2, 1, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_8.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_8.setText("")
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout.addWidget(self.pushButton_8, 2, 2, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_9.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_9.setText("")
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout.addWidget(self.pushButton_9, 2, 3, 1, 1)
        self.pushButton_10 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_10.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_10.setText("")
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout.addWidget(self.pushButton_10, 2, 4, 1, 1)
        self.pushButton_11 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_11.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_11.setText("")
        self.pushButton_11.setObjectName("pushButton_11")
        self.gridLayout.addWidget(self.pushButton_11, 2, 5, 1, 1)
        self.pushButton_12 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_12.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_12.setText("")
        self.pushButton_12.setObjectName("pushButton_12")
        self.gridLayout.addWidget(self.pushButton_12, 2, 7, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.layoutWidget)
        self.label_9.setStyleSheet("background-color: rgb(255, 255, 255);\n""font: 12pt \"黑体\";")
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 3, 0, 1, 1)
        self.pushButton_13 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_13.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_13.setText("")
        self.pushButton_13.setObjectName("pushButton_13")
        self.gridLayout.addWidget(self.pushButton_13, 3, 1, 1, 1)
        self.pushButton_14 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_14.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_14.setText("")
        self.pushButton_14.setObjectName("pushButton_14")
        self.gridLayout.addWidget(self.pushButton_14, 3, 2, 1, 1)
        self.pushButton_15 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_15.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_15.setText("")
        self.pushButton_15.setObjectName("pushButton_15")
        self.gridLayout.addWidget(self.pushButton_15, 3, 3, 1, 1)
        self.pushButton_16 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_16.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_16.setText("")
        self.pushButton_16.setObjectName("pushButton_16")
        self.gridLayout.addWidget(self.pushButton_16, 3, 4, 1, 1)
        self.pushButton_18 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_18.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_18.setText("")
        self.pushButton_18.setObjectName("pushButton_18")
        self.gridLayout.addWidget(self.pushButton_18, 3, 7, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.layoutWidget)
        self.label_10.setStyleSheet("background-color: rgb(255, 255, 255);\n""font: 12pt \"黑体\";")
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 4, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.layoutWidget)
        self.label_11.setStyleSheet("background-color: rgb(255, 255, 255);\n""font: 12pt \"黑体\";")
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 5, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.layoutWidget)
        self.label_12.setStyleSheet("background-color: rgb(255, 255, 255);\n""font: 12pt \"黑体\";")
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 6, 0, 1, 1)
        self.pushButton_19 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_19.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_19.setText("")
        self.pushButton_19.setObjectName("pushButton_19")
        self.gridLayout.addWidget(self.pushButton_19, 4, 1, 1, 1)
        self.pushButton_20 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_20.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_20.setText("")
        self.pushButton_20.setObjectName("pushButton_20")
        self.gridLayout.addWidget(self.pushButton_20, 4, 2, 1, 1)
        self.pushButton_21 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_21.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_21.setText("")
        self.pushButton_21.setObjectName("pushButton_21")
        self.gridLayout.addWidget(self.pushButton_21, 4, 3, 1, 1)
        self.pushButton_22 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_22.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_22.setText("")
        self.pushButton_22.setObjectName("pushButton_22")
        self.gridLayout.addWidget(self.pushButton_22, 4, 4, 1, 1)
        self.pushButton_23 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_23.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_23.setText("")
        self.pushButton_23.setObjectName("pushButton_23")
        self.gridLayout.addWidget(self.pushButton_23, 4, 5, 1, 1)
        self.pushButton_24 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_24.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_24.setText("")
        self.pushButton_24.setObjectName("pushButton_24")
        self.gridLayout.addWidget(self.pushButton_24, 4, 7, 1, 1)
        self.pushButton_25 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_25.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_25.setText("")
        self.pushButton_25.setObjectName("pushButton_25")
        self.gridLayout.addWidget(self.pushButton_25, 5, 1, 1, 1)
        self.pushButton_26 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_26.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_26.setText("")
        self.pushButton_26.setObjectName("pushButton_26")
        self.gridLayout.addWidget(self.pushButton_26, 5, 2, 1, 1)
        self.pushButton_27 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_27.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_27.setText("")
        self.pushButton_27.setObjectName("pushButton_27")
        self.gridLayout.addWidget(self.pushButton_27, 5, 3, 1, 1)
        self.pushButton_28 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_28.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_28.setText("")
        self.pushButton_28.setObjectName("pushButton_28")
        self.gridLayout.addWidget(self.pushButton_28, 5, 4, 1, 1)
        self.pushButton_29 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_29.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_29.setText("")
        self.pushButton_29.setObjectName("pushButton_29")
        self.gridLayout.addWidget(self.pushButton_29, 5, 5, 1, 1)
        self.pushButton_30 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_30.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_30.setText("")
        self.pushButton_30.setObjectName("pushButton_30")
        self.gridLayout.addWidget(self.pushButton_30, 5, 7, 1, 1)
        self.pushButton_31 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_31.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_31.setText("")
        self.pushButton_31.setObjectName("pushButton_31")
        self.gridLayout.addWidget(self.pushButton_31, 6, 1, 1, 1)
        self.pushButton_32 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_32.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_32.setText("")
        self.pushButton_32.setObjectName("pushButton_32")
        self.gridLayout.addWidget(self.pushButton_32, 6, 2, 1, 1)
        self.pushButton_33 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_33.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_33.setText("")
        self.pushButton_33.setObjectName("pushButton_33")
        self.gridLayout.addWidget(self.pushButton_33, 6, 3, 1, 1)
        self.pushButton_34 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_34.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_34.setText("")
        self.pushButton_34.setObjectName("pushButton_34")
        self.gridLayout.addWidget(self.pushButton_34, 6, 4, 1, 1)
        self.pushButton_35 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_35.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_35.setText("")
        self.pushButton_35.setObjectName("pushButton_35")
        self.gridLayout.addWidget(self.pushButton_35, 6, 5, 1, 1)
        self.pushButton_36 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_36.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_36.setText("")
        self.pushButton_36.setObjectName("pushButton_36")
        self.gridLayout.addWidget(self.pushButton_36, 6, 7, 1, 1)
        self.pushButton_17 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_17.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_17.setText("")
        self.pushButton_17.setObjectName("pushButton_17")
        self.gridLayout.addWidget(self.pushButton_17, 3, 5, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_6.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_6.setText("")
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 1, 7, 1, 1)
        self.pushButton_37 = QtWidgets.QPushButton(Form)
        self.pushButton_37.setGeometry(QtCore.QRect(180, 290, 141, 41))
        self.pushButton_37.setStyleSheet("font: 18pt \"楷体\";\n""background-color: rgb(255, 255, 255);")
        self.pushButton_37.setObjectName("pushButton_37")

        QtCore.QMetaObject.connectSlotsByName(Form)

        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "cmz_选座界面"))
        self.label_13.setText(_translate("Form", "座位选择"))
        self.pushButton.setText(_translate("Form", "选择完成"))
        self.label.setText(_translate("Form", " 1"))
        self.label_2.setText(_translate("Form", " 2"))
        self.label_3.setText(_translate("Form", " 3"))
        self.label_4.setText(_translate("Form", " 4"))
        self.label_5.setText(_translate("Form", " 5"))
        self.label_6.setText(_translate("Form", " 6"))
        self.label_7.setText(_translate("Form", "1"))
        self.label_8.setText(_translate("Form", "2"))
        self.label_9.setText(_translate("Form", "3"))
        self.label_10.setText(_translate("Form", "4"))
        self.label_11.setText(_translate("Form", "5"))
        self.label_12.setText(_translate("Form", "6"))
        self.pushButton_37.setText(_translate("Form", "查看信息"))

        self.pushButton_1.clicked.connect(self.pushButton_1_click)
        self.pushButton_2.clicked.connect(self.pushButton_2_click)
        self.pushButton_3.clicked.connect(self.pushButton_3_click)
        self.pushButton_4.clicked.connect(self.pushButton_4_click)
        self.pushButton_5.clicked.connect(self.pushButton_5_click)
        self.pushButton_6.clicked.connect(self.pushButton_6_click)
        self.pushButton_7.clicked.connect(self.pushButton_7_click)
        self.pushButton_8.clicked.connect(self.pushButton_8_click)
        self.pushButton_9.clicked.connect(self.pushButton_9_click)
        self.pushButton_10.clicked.connect(self.pushButton_10_click)
        self.pushButton_11.clicked.connect(self.pushButton_11_click)
        self.pushButton_12.clicked.connect(self.pushButton_12_click)
        self.pushButton_13.clicked.connect(self.pushButton_13_click)
        self.pushButton_14.clicked.connect(self.pushButton_14_click)
        self.pushButton_15.clicked.connect(self.pushButton_15_click)
        self.pushButton_16.clicked.connect(self.pushButton_16_click)
        self.pushButton_17.clicked.connect(self.pushButton_17_click)
        self.pushButton_18.clicked.connect(self.pushButton_18_click)
        self.pushButton_19.clicked.connect(self.pushButton_19_click)
        self.pushButton_20.clicked.connect(self.pushButton_20_click)
        self.pushButton_21.clicked.connect(self.pushButton_21_click)
        self.pushButton_22.clicked.connect(self.pushButton_22_click)
        self.pushButton_23.clicked.connect(self.pushButton_23_click)
        self.pushButton_24.clicked.connect(self.pushButton_24_click)
        self.pushButton_25.clicked.connect(self.pushButton_25_click)
        self.pushButton_26.clicked.connect(self.pushButton_26_click)
        self.pushButton_27.clicked.connect(self.pushButton_27_click)
        self.pushButton_28.clicked.connect(self.pushButton_28_click)
        self.pushButton_29.clicked.connect(self.pushButton_29_click)
        self.pushButton_30.clicked.connect(self.pushButton_30_click)
        self.pushButton_31.clicked.connect(self.pushButton_31_click)
        self.pushButton_32.clicked.connect(self.pushButton_32_click)
        self.pushButton_33.clicked.connect(self.pushButton_33_click)
        self.pushButton_34.clicked.connect(self.pushButton_34_click)
        self.pushButton_35.clicked.connect(self.pushButton_35_click)
        self.pushButton_36.clicked.connect(self.pushButton_36_click)
        self.pushButton_37.clicked.connect(lambda : search_seat_interface_2.show())

        # 连接数据库
        self.db = pymysql.connect(
            host="localhost",
            user="root",
            password="123456",
            database="information",
        )
        # 获取操作数据库的游标
        self.cursor = self.db.cursor()

        ui_buy_ticket_window.pushButton.pressed.connect(ui_buy_ticket_window.judge_movie_name)
        ui_buy_ticket_window.pushButton_2.pressed.connect(ui_buy_ticket_window.judge_movie_name)
        ui_buy_ticket_window.pushButton_3.pressed.connect(ui_buy_ticket_window.judge_movie_name)
        ui_buy_ticket_window.pushButton_4.pressed.connect(ui_buy_ticket_window.judge_movie_name)
        ui_buy_ticket_window.pushButton_5.pressed.connect(ui_buy_ticket_window.judge_movie_name)
        ui_buy_ticket_window.pushButton_6.pressed.connect(ui_buy_ticket_window.judge_movie_name)
        ui_buy_ticket_window.pushButton_7.pressed.connect(ui_buy_ticket_window.judge_movie_name)
        ui_buy_ticket_window.pushButton_8.pressed.connect(ui_buy_ticket_window.judge_movie_name)




    def pushButton_1_click(self):
            self.pushButton_1.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_1.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '1', '1')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 1 1

    def pushButton_2_click(self):
            self.pushButton_2.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_2.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '1', '2')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 1 2

    def pushButton_3_click(self):
            self.pushButton_3.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_3.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '1', '3')
            self.cursor.execute(sql, val)
            self.db.commit()

        # 1 3

    def pushButton_4_click(self):
            self.pushButton_4.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_4.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '1', '4')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 1 4

    def pushButton_5_click(self):
            self.pushButton_5.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_5.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '1', '5')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 1 5

    def pushButton_6_click(self):
            self.pushButton_6.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_6.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '1', '6')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 1 6

    def pushButton_7_click(self):
            self.pushButton_7.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_7.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '2', '1')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 2 1

    def pushButton_8_click(self):
            self.pushButton_8.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_8.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '2', '2')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 2 2

    def pushButton_9_click(self):
            self.pushButton_9.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_9.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '2', '3')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 2 3

    def pushButton_10_click(self):
            self.pushButton_10.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_10.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '2', '4')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 2 4

    def pushButton_11_click(self):
            self.pushButton_11.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_11.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '2', '5')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 2 5

    def pushButton_12_click(self):
            self.pushButton_12.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_12.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '2', '6')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 2 6

    def pushButton_13_click(self):
            self.pushButton_13.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_13.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '3', '1')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 3 1

    def pushButton_14_click(self):
            self.pushButton_14.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_14.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '3', '2')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 3 2

    def pushButton_15_click(self):
            self.pushButton_15.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_15.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '3', '3')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 3 3

    def pushButton_16_click(self):
            self.pushButton_16.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_16.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '3', '4')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 3 4

    def pushButton_17_click(self):
            self.pushButton_17.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_17.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '3', '5')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 3 5

    def pushButton_18_click(self):
            self.pushButton_18.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_18.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '3', '6')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 3 6

    def pushButton_19_click(self):
            self.pushButton_19.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_19.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '4', '1')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 4 1

    def pushButton_20_click(self):
            self.pushButton_20.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_20.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '4', '2')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 4 2

    def pushButton_21_click(self):
            self.pushButton_21.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_21.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '4', '3')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 4 3

    def pushButton_22_click(self):
            self.pushButton_22.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_22.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '4', '4')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 4 4

    def pushButton_23_click(self):
            self.pushButton_23.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_23.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '4', '5')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 4 5

    def pushButton_24_click(self):
            self.pushButton_24.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_24.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '4', '6')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 4 6

    def pushButton_25_click(self):
            self.pushButton_25.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_25.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '5', '1')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 5 1

    def pushButton_26_click(self):
            self.pushButton_26.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_26.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '5', '2')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 5 2

    def pushButton_27_click(self):
            self.pushButton_27.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_27.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '5', '3')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 5 3

    def pushButton_28_click(self):
            self.pushButton_28.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_28.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '5', '4')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 5 4

    def pushButton_29_click(self):
            self.pushButton_29.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_29.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '5', '5')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 5 5

    def pushButton_30_click(self):
            self.pushButton_30.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_30.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '5', '6')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 5 6

    def pushButton_31_click(self):
            self.pushButton_31.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_31.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '6', '1')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 6 1

    def pushButton_32_click(self):
            self.pushButton_32.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_32.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '6', '2')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 6 2

    def pushButton_33_click(self):
            self.pushButton_33.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_33.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '6', '3')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 6 3

    def pushButton_34_click(self):
            self.pushButton_34.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_34.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '6', '4')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 6 4

    def pushButton_35_click(self):
            self.pushButton_35.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_35.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '6', '5')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 6 5

    def pushButton_36_click(self):
            self.pushButton_36.setStyleSheet("background-color:rgb(255, 102, 102)")
            self.pushButton_36.setText("已选")
            sql = "insert into select_information (账号, 电影, 行, 列) values (%s, %s, %s, %s)"
            val = (ui_sign_window.get_sign_account, ui_buy_ticket_window.label_name, '6', '6')
            self.cursor.execute(sql, val)
            self.db.commit()
        # 6 6


# 调出选作信息
class Ui_search_seat_information(QMainWindow):
    def __init__(self):
        super().__init__()

        # 添加一个 QTableWidget 控件用于显示数据
        self.table_widget = QTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.table_widget.setFixedSize(475, 300)
        # 设置字体
        font = QFont('楷体', 12, QFont.Bold)
        self.table_widget.setFont(font)
        db = pymysql.connect(host="localhost", user="root", password="123456", db="information")
        cursor = db.cursor()
        cursor.execute("select * from select_information")
        # 读取查询结果并将其显示在表格控件中
        num_rows = cursor.rowcount
        self.table_widget.setRowCount(num_rows)
        self.table_widget.setColumnCount(4)
        # 设置列宽
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        self.table_widget.setHorizontalHeaderLabels(['用户名', '电影名', '行', '列'])
        for i, row in enumerate(cursor.fetchall()):
            for j, item in enumerate(row):
                self.table_widget.setItem(i, j, QTableWidgetItem(str(item)))

        # 关闭数据库连接
        db.close()


# 登陆界面
class Ui_sign(object):
    def sign_ui(self, Main_Window):
        Main_Window.setObjectName("Main_Window")
        Main_Window.setFixedSize(372, 207)
        Main_Window.setWindowIcon(QIcon("780.ico"))

        # 连接数据库
        self.db = pymysql.connect(
            host="localhost",
            user="root",
            password="123456",
            database="Select_Ticket_System",
        )

        # 获取操作数据库的游标
        self.cursor = self.db.cursor()

        self.lineEdit = QtWidgets.QLineEdit(Main_Window)
        self.lineEdit.setGeometry(QtCore.QRect(101, 21, 250, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("请输入账号")
        self.pushButton = QtWidgets.QPushButton(Main_Window)
        self.pushButton.setGeometry(QtCore.QRect(10, 130, 351, 51))
        self.pushButton.setStyleSheet("font: 20pt \"楷体\";\n""background-color: rgb(85, 170, 255);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.check_sign)

        self.label = QtWidgets.QLabel(Main_Window)
        self.label.setGeometry(QtCore.QRect(10, 20, 84, 27))
        self.label.setStyleSheet("font: 16pt \"楷体\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Main_Window)
        self.label_2.setGeometry(QtCore.QRect(9, 79, 84, 27))
        self.label_2.setStyleSheet("font: 16pt \"楷体\";")
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(Main_Window)
        self.lineEdit_2.setGeometry(QtCore.QRect(100, 80, 250, 30))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setPlaceholderText("请输入密码")

        self.pushButton_2 = QtWidgets.QPushButton(Main_Window)
        self.pushButton_2.setGeometry(QtCore.QRect(-7, 182, 91, 31))
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 255, 255);\n""font: 10pt \"楷体\";")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(lambda: register_interface.show())

        self.pushButton_3 = QtWidgets.QPushButton(Main_Window)
        self.pushButton_3.setGeometry(QtCore.QRect(288, 182, 93, 28))
        self.pushButton_3.setStyleSheet("background-color: rgb(255, 255, 255);\n""font: 10pt \"楷体\";")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.search_password)

        self.retranslateUi(Main_Window)
        QtCore.QMetaObject.connectSlotsByName(Main_Window)



    def retranslateUi(self, Main_Window):
        _translate = QtCore.QCoreApplication.translate
        Main_Window.setWindowTitle(_translate("Main_Window", "cmz_登陆界面"))
        self.pushButton.setText(_translate("Main_Window", "登录"))
        self.label.setText(_translate("Main_Window", "账号："))
        self.label_2.setText(_translate("Main_Window", "密码："))
        self.pushButton_2.setText(_translate("Main_Window", "注册账号"))
        self.pushButton_3.setText(_translate("Main_Window", "忘记密码"))

    def clear_user_information(self):
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')

    def check_sign(self):
        self.get_sign_account = self.lineEdit.text()
        self.get_sign_password = self.lineEdit_2.text()

        # 查询用户 密码
        query = f"select password from user where account = '{self.get_sign_account}'"
        self.cursor.execute(query)
        list = self.cursor.fetchone()
        # print(query)
        # print(list[0])
        # print(list)

        # 查找用户 账号
        with open('result.txt', 'r') as f:
            data = f.readlines()  # 读取整个文件内容并按行分割成列表
        new_data = []  # 声明一个新的列表，用于存储处理后的数据
        for line in data:
            new_line_1 = re.sub(r"['()\n]", "", line)  # 使用正则表达式替换对应的符号
            new_line_2 = new_line_1.split(',')[0]
            new_data.append(new_line_2)  # 将处理后的行添加到新的列表中
            # new_data是注册用户的  用户名列表
        while True:
            is_user = False
            for check in new_data:
                if check == self.get_sign_account:
                    is_user = True

            if is_user == False:
                box_sign_3 = QMessageBox()
                box_sign_3.setWindowTitle("提示")
                box_sign_3.setText("用户名不存在！")
                box_sign_3.setStandardButtons(QMessageBox.Yes)
                box_sign_3.exec()
                self.clear_user_information()
                return

            if self.get_sign_account == "" or self.get_sign_password == "":
                box_sign_0 = QMessageBox()
                box_sign_0.setWindowTitle("提示")
                box_sign_0.setText("请完整输入！")
                box_sign_0.setStandardButtons(QMessageBox.Yes)
                box_sign_0.exec()
                break

            if list[0] == self.get_sign_password:
                box_sign_1 = QMessageBox()
                box_sign_1.setWindowTitle("提示")
                box_sign_1.setText("登陆成功！")
                box_sign_1.setStandardButtons(QMessageBox.Yes)
                box_sign_1.exec()
                buy_ticket_interface.show()
                sign_interface.close()
                break

            else:
                box_sign_2 = QMessageBox()
                box_sign_2.setWindowTitle("提示")
                box_sign_2.setText("账号或密码错误！")
                box_sign_2.setStandardButtons(QMessageBox.Yes)
                box_sign_2.exec()
                self.cursor.close()
                self.cursor.close()
                self.clear_user_information()
                break
# 找密码
    def search_password(self):
        self.get_sign_account_search = self.lineEdit.text()
        # 查询用户 密码
        query = f"select password from user where account = '{self.get_sign_account_search}'"
        self.cursor.execute(query)
        list = self.cursor.fetchone()

        box_password = QMessageBox()
        box_password.setWindowTitle("提示")
        box_password.setText(f"尊敬的：{self.lineEdit.text()}\n        您的密码为：{list[0]}")
        box_password.setStandardButtons(QMessageBox.Yes)
        box_password.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)

# 具体的类
    sign_interface = QWidget()
    register_interface = QWidget()
    buy_ticket_interface = QWidget()
    select_seat_interface = QWidget()
    select_seat_interface_2 = QWidget()
    select_seat_interface_3 = QWidget()
    select_seat_interface_4 = QWidget()
    select_seat_interface_5 = QWidget()
    select_seat_interface_6 = QWidget()
    select_seat_interface_7 = QWidget()
    select_seat_interface_8 = QWidget()
    search_seat_interface = QWidget()
    search_seat_interface_2 = Ui_search_seat_information()


# 调用ui
    ui_sign_window = Ui_sign()
    ui_register_window = Ui_register()
    ui_buy_ticket_window = Ui_buy_ticket()
    ui_select_seat_window = Ui_select_seat()
    ui_select_seat_window_2 = Ui_select_seat()
    ui_select_seat_window_3 = Ui_select_seat()
    ui_select_seat_window_4 = Ui_select_seat()
    ui_select_seat_window_5 = Ui_select_seat()
    ui_select_seat_window_6 = Ui_select_seat()
    ui_select_seat_window_7 = Ui_select_seat()
    ui_select_seat_window_8 = Ui_select_seat()

# 用ui的函数
    ui_sign_window.sign_ui(sign_interface)
    ui_register_window.register_ui(register_interface)
    ui_buy_ticket_window.buy_ticket_ui(buy_ticket_interface)
    ui_select_seat_window.select_seat_ui(select_seat_interface)
    ui_select_seat_window_2.select_seat_ui(select_seat_interface_2)
    ui_select_seat_window_3.select_seat_ui(select_seat_interface_3)
    ui_select_seat_window_4.select_seat_ui(select_seat_interface_4)
    ui_select_seat_window_5.select_seat_ui(select_seat_interface_5)
    ui_select_seat_window_6.select_seat_ui(select_seat_interface_6)
    ui_select_seat_window_7.select_seat_ui(select_seat_interface_7)
    ui_select_seat_window_8.select_seat_ui(select_seat_interface_8)

# 打印出窗口界面
    sign_interface.show()

    sys.exit(app.exec_())

