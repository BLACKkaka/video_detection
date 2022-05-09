
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import QVideoWidget

class Video:
    # def __init__(self, path):
    #     self.path = path 
    
    def __init__(self):
        super(Video,self).__init__()
        self.setupUi(self)
        #按钮初始化
        self.PushButtonInit()
        #进度条初始化
        self.ProgressBarInit()
        ####播放器、播放列表初始化
        self.mplayer = QMediaPlayer()
        self.ListWidgetInit()
        self.mplayList.setCurrentIndex(0)
        #控件初始化
        self.mVideoWin = QVideoWidget(self)
        self.mVideoWin.setGeometry(0,0,411,411)
        #设置输出窗体
        self.mplayer.setVideoOutput(self.mVideoWin)
        #信号、槽
        self.play.clicked.connect(self.PlayVideo)
        self.pause.clicked.connect(self.PauseVideo)
        #......

    def PushButtonInit(self):
        self.play = QPushButton(self)
        self.play.setGeometry(90,420,50,20)
        self.play.setText("Play")
        self.play.show()
        self.pause = QPushButton(self)
        self.pause.setGeometry(0,420,50,20)
        self.pause.setText("pause")
        self.pause.show()

    def ProgressBarInit(self):
        self.Slider = QSlider(self)
        self.Slider.setGeometry(150,420,200,20)
        self.Slider.setRange(0,100)
        self.Slider.show()

    def ListWidgetInit(self):
        pass
    def PlayVideo(self):
        self.mplayer.play()
    def PauseVideo(self):
        self.mplayer.pause()
   