# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'congratulation.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
import numpy as np

class Congrat_Window(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.ui = Ui_Congrat(self)
        self.ui.setupUi(self)
    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Enter:
            self.close()
            self.parent.parent.Reload()
            self.parent.parent.sound.stop()

    def closeEvent(self, event):
        self.parent.parent.Reload()
        event.accept()

class Ui_Congrat(object):
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        # qApp.installEventFilter(self)
    
    def setupUi(self, Form):

        Form.setObjectName("Form")
        Form.resize(583, 387)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 30, 561, 341))
        self.label.setText("")

        # Add gif
        gif = QtGui.QMovie('assets/%s.gif'%(str(np.random.randint(12))))
        self.label.setMovie(gif)
        gif.start()

        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(150, 280, 371, 51))
        font = QtGui.QFont()
        font.setFamily("Brush Script MT")
        font.setPointSize(24)
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Congratulation :3"))
        self.label_2.setText(_translate("Form", "CONGRATULATION"))

