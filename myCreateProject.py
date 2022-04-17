from crtProject import Ui_Dialog
from PyQt5.QtWidgets import QDialog

class myCreateProjects(Ui_Dialog, QDialog):
    def __init__(self):
        super(Ui_Dialog, self).__init__()
        self.setupUi(self)
