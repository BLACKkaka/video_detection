import os
import sys
import time

import cv2
import torch
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication
from PyQt5 import QtGui

from models.yolox.yoloxs import Predictor, imageflow_demo, CLASSES
from test import Ui_MainWindow
from myCreateProject import myCreateProjects
from Project import Project


class myMainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.sld_video_pressed = False  #判断当前进度条识别否被鼠标点击
        # self.player = QMediaPlayer()
        # self.player.setVideoOutput(self.widget)  # 父类继承的
        self.action.triggered.connect(self.createProject)
        self.action_2.triggered.connect(self.selectProject)
        self.action_3.triggered.connect(self.saveProject)
        self.action_5.triggered.connect(self.inferenceVideo)
        self.pushButton_2.clicked.connect(self.playVideo)       # play
        self.pushButton.clicked.connect(self.pauseVideo)       # pause
        # self.player.positionChanged.connect(self.changeSlide)  # change Slide
        self.horizontalSlider_2.setTracking(False)
        self.horizontalSlider_2.sliderReleased.connect(self.releaseSlider)
        self.horizontalSlider_2.sliderPressed.connect(self.pressSlider)
        self.horizontalSlider_2.sliderMoved.connect(self.moveSlider)   # 进度条拖拽跳转
        self.horizontalSlider_2.ClickedValue.connect(self.clickedSlider)  # 进度条点击跳转
        # 子窗口们
        self.crtPrj = myCreateProjects()
        # 注释掉声音控件，因为管道视频没有声音
        # self.horizontalSlider.valueChanged.connect(self.volumeChange)

    def openVideoFile(self):
        # self.player.setMedia(QMediaContent(QFileDialog.getOpenFileUrl()[0]))  # 选取视频文件
        # 用于测试功能，直接播放
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile('./resources/remove1.avi'))) #直接播放
        self.player.play()  # 播放视频
        print(self.player.availableMetaData())

    def playVideo(self):
        self.player.play()

    def pauseVideo(self):
        self.player.pause()

    # def changeSlide(self, position):
    #     if not self.sld_video_pressed:  # 进度条被鼠标点击时不更新
    #         self.vidoeLength = self.player.duration()+0.1
    #         self.horizontalSlider_2.setValue(round((position/self.vidoeLength)*100))
    #         self.label_17.setText("%.2f%%" % ((position/self.vidoeLength)*100))

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
        self.crtPrj.show()

    #2022-3-8 选择项目打开
    def selectProject(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,"选取文件","./projects/","All Files (*);;Text Files (*.txt)")
        with open(fileName1,'r') as f:
            for item in f.readlines():
                pass
            #这里看看如何做反序列化

    #2022-3-8 调用序列化方法，将项目保存到文件中
    def saveProject(self):
        # projectName = getnamefromlist
        projectName = Project()
        projectName.Serialization()

    def inferenceVideo(self):
        file_name = "./models/yolox/myyolox/"
        os.makedirs(file_name, exist_ok=True)
        vis_folder = os.path.join(file_name, "vis_res")
        os.makedirs(vis_folder, exist_ok=True)

        model = torch.load("./models/yolox/yolox_detector.pth")
        print("模型加载完成")
        model.cuda()
        # model.half()
        model.eval()
        predictor = Predictor(model, CLASSES)
        current_time = time.localtime()

        video_path = "./resources/remove1.avi"
        cap = cv2.VideoCapture(video_path)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float
        fps = cap.get(cv2.CAP_PROP_FPS)
        save_folder = os.path.join(
            vis_folder, time.strftime("%Y_%m_%d_%H_%M_%S", current_time)
        )
        os.makedirs(save_folder, exist_ok=True)
        # save_path需要看软件需要
        save_path = os.path.join(save_folder, video_path.split("/")[-1])
        vid_writer = cv2.VideoWriter(
            save_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (int(width), int(height))
        )
        print("开始预测")
        while True:
            ret_val, frame = cap.read()
            if ret_val:
                outputs, img_info = predictor.inference(frame)
                result_frame = predictor.visual(outputs[0], img_info, predictor.confthre)
                _image = QtGui.QImage(result_frame[:], result_frame.shape[1], result_frame.shape[0], result_frame.shape[1] * 3,
                                      QtGui.QImage.Format_RGB888)  # pyqt5转换成自己能放的图片格式
                jpg_out = QtGui.QPixmap(_image).scaled(self.label.width(), self.label.height())  # 设置图片大小
                self.label.setPixmap(jpg_out)  # 设置图片显示
                vid_writer.write(result_frame)
                # 这些地方应该能改一改作为pyqt暂停的信号槽
                # ch = cv2.waitKey(1)
                # if ch == 27 or ch == ord("q") or ch == ord("Q"):
                #     break
            else:
                break
        print("检测完成")

    # def volumeChange(self, position):
    #     volume = round(position/self.sld_audio.maximum()*100)
    #     self.player.setVolume(volume)
    #     self.label_18.setText("volume:"+str(volume)+"%")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    video_gui = myMainWindow()
    video_gui.show()
    sys.exit(app.exec_())