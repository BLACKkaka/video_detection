import os
import pickle

from Video import Video

class Project:
    # def __init__(self):
    #     pass

    def __init__(self, prj_name, vdo_list):
        self.videoList = []
        self.name = prj_name
        for item in vdo_list:
            v = Video(item)
            self.videoList.append(v)

    # 如果该视频已经不存在了，就删除这个视频对象
    def checkVideo(self):
        for item in self.videoList:
            if os.path.exists(item.path) == False:
                self.videoList.remove(item)

    # 工程对象序列化
    def Serialization(self):
        with open("./projects/" + self.name + ".pickle", "wb") as f:
            pickle.dump(self,f)


def createProject():
    # 创建项目的准备工作，不允许项目同名
    # 通过序列化做持久
    if os.path.exists("./projects/") == False:
        os.mkdir("./projects/")
        projectsList = []
    else:
        projectsList = os.listdir("./projects/")
    print(len(projectsList))

createProject()