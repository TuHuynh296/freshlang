# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testFrame.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(456, 388)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.openGLWidget = QtWidgets.QOpenGLWidget(Form)
        self.openGLWidget.setObjectName("openGLWidget")
        self.horizontalLayout.addWidget(self.openGLWidget)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(50, 70, 47, 16))
        self.label.setObjectName("label")
        self.calendarWidget = QtWidgets.QCalendarWidget(self)
        self.calendarWidget.setGeometry(QtCore.QRect(0, 0, 312, 183))
        self.calendarWidget.setObjectName("calendarWidget")
        self.calendarWidget.raise_()
        self.label.raise_()
        self.horizontalLayout.addWidget(self.frame)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

