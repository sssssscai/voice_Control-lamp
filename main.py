import sys

from PyQt5 import QtCore, QtGui, QtWidgets
import multiprocessing
import time
from multiprocessing import Process,Value

from PyQt5.QtCore import QThread, pyqtSignal, QTimer
import speech_recognition as sr
import logging
from aip import AipSpeech
from tkinter import *
import socket

logging.basicConfig(level=logging.DEBUG)


def voice_recognition(n):
    BAIDU_APP_ID = '28728033'
    BAIDU_API_KEY = 'byG5yX4YPPYZg09oD9ixbmKF'
    BAIDU_SECRET_KEY = '4vFLMVeNBof1Qw821bQPjUWFGjuZ3kjy'
    aip_speech = AipSpeech(BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_KEY)
    r = sr.Recognizer()
    mic = sr.Microphone(sample_rate=16000)
    while True:
        logging.info('录音中...')
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        logging.info('录音结束，识别中...')
        audio_data = audio.get_wav_data()
        ret = aip_speech.asr(audio_data, 'wav', 16000, {'dev_pid': 1536, })
        if ret and ret['err_no'] == 0:
            result = ret['result'][0]
            print("语音识别结果为:" + str(result))
            n.append(str(result))
        else:
            print(ret['err_msg'])
        logging.info('end')
    p.join()
    return

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(469, 541)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(11, 11, 113, 16))
        self.label.setObjectName("label")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setEnabled(True)
        self.label_5.setGeometry(QtCore.QRect(11, 33, 450, 25))
        self.label_5.setStyleSheet("background-color: white")
        self.label_5.setFrameShape(QtWidgets.QFrame.Box)
        self.label_5.setObjectName("label_5")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(11, 62, 128, 16))
        self.label_2.setObjectName("label_2")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(11, 84, 450, 25))
        self.label_6.setStyleSheet("background-color: white")
        self.label_6.setFrameShape(QtWidgets.QFrame.Box)
        self.label_6.setObjectName("label_6")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(-10, 110, 481, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(11, 270, 98, 16))
        self.label_4.setObjectName("label_4")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(11, 300, 450, 192))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(11, 190, 450, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(11, 230, 450, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 130, 451, 39))
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.checkBox = QtWidgets.QCheckBox(self.widget)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_2.addWidget(self.checkBox)
        self.checkBox_2 = QtWidgets.QCheckBox(self.widget)
        self.checkBox_2.setObjectName("checkBox_2")
        self.horizontalLayout_2.addWidget(self.checkBox_2)
        self.checkBox_3 = QtWidgets.QCheckBox(self.widget)
        self.checkBox_3.setObjectName("checkBox_3")
        self.horizontalLayout_2.addWidget(self.checkBox_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 469, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.checkBox.clicked.connect(lambda: self.f(self.checkBox))
        self.checkBox_2.clicked.connect(lambda: self.f(self.checkBox_2))
        self.checkBox_3.clicked.connect(lambda: self.f(self.checkBox_3))
        self.pushButton.clicked.connect(lambda: self.open_light())
        self.pushButton_2.clicked.connect(lambda: self.close_light())
        self.checkBox_3.setChecked(True)
        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        self.textBrowser_text="";
        self.share_var_pos=0;
        self.share_var = multiprocessing.Manager().list()
        voice_process= Process(target=voice_recognition, args=(self.share_var,))
        voice_process.start()

        self.light_status=0 #灯泡状态 1 代表亮灯 -1熄灭 0代表未知

        self.Server_IP="192.168.10.125" #服务器IP以及端口
        self.light_IP="" #灯泡IP以及端口
        self.button_status=0; #按钮请求状态 1代表请求开灯 0代表关灯
        self.tcp_client_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 2 通过客户端套接字的connect方法与服务器套接字建立连接
        # 参数介绍：前面的ip地址代表服务器的ip地址，后面的61234代表服务端的端口号 。

        self.tcp_client_1.connect((self.Server_IP, 51234))
        self.send_data = "你好，我是主机".encode(encoding='utf-8')
        self.tcp_client_1.send(self.send_data)
        self.recv_data = self.tcp_client_1.recv(1024)
        self.light_IP= self.recv_data

        self.label_5.setText("已成功连接服务器，IP地址以及端口号为"+"192.168.10.125, 61572")
        self.label_5.repaint()
        temp=str(self.recv_data)
        self.label_6.setText("已成功连接灯泡，IP地址及端口号为" +temp[1:] )
        self.label_6.repaint()
    def f(self,x):
        x.setChecked(not x.isChecked())
        return;


    def showTime(self):
        lenx=len(self.share_var)
        for i in range(self.share_var_pos,lenx):
            self.textBrowser_text = self.textBrowser_text + self.share_var[i];

        #print(self.textBrowser_text)
        if(self.textBrowser_text!=""):
            self.textBrowser.append(self.textBrowser_text)
        if(self.textBrowser_text in ["开灯","开机","启动","开启电灯","打开电灯","打开","开启灯泡"]):
            self.button_status=1
        elif (self.textBrowser_text in ["关灯","关机", "结束", "关闭电灯", "关掉电灯", "关掉"]):
            self.button_status = 0
        self.textBrowser_text=""
        self.share_var_pos=lenx
        #self.share_var=multiprocessing.Manager().list()
        #x = "open"
        #send_data = x.encode(encoding='utf-8')
        if self.button_status==1:
            x = "open"
            send_data = x.encode(encoding='utf-8')
            self.tcp_client_1.send(send_data)
            self.checkBox.setChecked(True)
            self.checkBox_2.setChecked(False)
            self.checkBox_3.setChecked(False)
        elif self.button_status==0:
            x = "close"
            send_data = x.encode(encoding='utf-8')
            self.tcp_client_1.send(send_data)
            self.checkBox.setChecked(False)
            self.checkBox_2.setChecked(True)
            self.checkBox_3.setChecked(False)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "远程灯泡控制系统"))
        self.label.setText(_translate("MainWindow", "服务器连接状态:"))
        self.label_5.setText(_translate("MainWindow", "未连接服务器"))
        self.label_2.setText(_translate("MainWindow", "远程灯泡连接状态:"))
        self.label_6.setText(_translate("MainWindow", "未连接灯泡"))
        self.label_4.setText(_translate("MainWindow", "语音识别结果:"))
        self.pushButton.setText(_translate("MainWindow", "开启灯泡"))
        self.pushButton_2.setText(_translate("MainWindow", "关闭灯泡"))
        self.label_3.setText(_translate("MainWindow", "灯泡当前情况:"))
        self.checkBox.setText(_translate("MainWindow", "亮灯"))
        self.checkBox_2.setText(_translate("MainWindow", "熄灭"))
        self.checkBox_3.setText(_translate("MainWindow", "未知"))

    def open_light(self):
        self.button_status=1
    def close_light(self):
        self.button_status=0


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    Ui = Ui_MainWindow()
    Ui.setupUi(MainWindow)
    #显示窗口并释放资源
    MainWindow.show()
    sys.exit(app.exec_())
  
