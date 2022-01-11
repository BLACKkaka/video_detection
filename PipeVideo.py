import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication

from test import Ui_MainWindow
from myCreateProject import myCreateProjects


class myMainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.sld_video_pressed = False  #判断当前进度条识别否被鼠标点击
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.widget)  # 父类继承的
        # 暂时绑定到“新建工程”按钮上
        self.action.triggered.connect(self.createProject)
        self.pushButton_2.clicked.connect(self.playVideo)       # play
        self.pushButton.clicked.connect(self.pauseVideo)       # pause
        self.player.positionChanged.connect(self.changeSlide)  # change Slide
        self.horizontalSlider_2.setTracking(False)
        self.horizontalSlider_2.sliderReleased.connect(self.releaseSlider)
        self.horizontalSlider_2.sliderPressed.connect(self.pressSlider)
        self.horizontalSlider_2.sliderMoved.connect(self.moveSlider)   # 进度条拖拽跳转
        self.horizontalSlider_2.ClickedValue.connect(self.clickedSlider)  # 进度条点击跳转
        # 注释掉声音控件，因为管道视频没有声音
        # self.horizontalSlider.valueChanged.connect(self.volumeChange)

    def openVideoFile(self):
        # self.player.setMedia(QMediaContent(QFileDialog.getOpenFileUrl()[0]))  # 选取视频文件
        # 用于测试功能，直接播放
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(r'C:\Users\coder\PycharmProjects\pyqt\resources\test1.mp4'))) #直接播放
        self.player.play()  # 播放视频
        print(self.player.availableMetaData())

    def playVideo(self):
        self.player.play()

    def pauseVideo(self):
        self.player.pause()


    def changeSlide(self, position):
        if not self.sld_video_pressed:  # 进度条被鼠标点击时不更新
            self.vidoeLength = self.player.duration()+0.1
            self.horizontalSlider_2.setValue(round((position/self.vidoeLength)*100))
            self.label_17.setText("%.2f%%" % ((position/self.vidoeLength)*100))

    def releaseSlider(self):
        self.sld_video_pressed = False

    def pressSlider(self):
        self.sld_video_pressed = True
        print("pressed")

    def moveSlider(self, position):
        self.sld_video_pressed = True
        if self.player.duration() > 0:  # 开始播放后才允许进行跳转
            video_position = int((position / 100) * self.player.duration())
            self.player.setPosition(video_position)
            self.label_17.setText("%.2f%%" % position)

    def clickedSlider(self, position):
        if self.player.duration() > 0:  # 开始播放后才允许进行跳转
            video_position = int((position / 100) * self.player.duration())
            self.player.setPosition(video_position)
            self.label_17.setText("%.2f%%" % position)
        else:
            self.horizontalSlider_2.setValue(0)


    def createProject(self):
        dialog = myCreateProjects()
        dialog.setupUi(myMainWindow)

    # def volumeChange(self, position):
    #     volume = round(position/self.sld_audio.maximum()*100)
    #     self.player.setVolume(volume)
    #     self.label_18.setText("volume:"+str(volume)+"%")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    vieo_gui = myMainWindow()
    vieo_gui.show()
    sys.exit(app.exec_())