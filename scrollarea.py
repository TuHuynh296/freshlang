# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scrollarea.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(450, 339)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 430, 319))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout.addWidget(self.checkBox)
        self.pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkBox_2 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_2.setObjectName("checkBox_2")
        self.horizontalLayout_2.addWidget(self.checkBox_2)
        self.pushButton_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.checkBox_3 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_3.setObjectName("checkBox_3")
        self.horizontalLayout_3.addWidget(self.checkBox_3)
        self.pushButton_3 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_3.addWidget(self.pushButton_3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.checkBox_4 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_4.setObjectName("checkBox_4")
        self.horizontalLayout_4.addWidget(self.checkBox_4)
        self.pushButton_4 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_4.addWidget(self.pushButton_4)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.checkBox_5 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_5.setObjectName("checkBox_5")
        self.horizontalLayout_5.addWidget(self.checkBox_5)
        self.pushButton_5 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_5.addWidget(self.pushButton_5)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.checkBox.setText(_translate("Form", "CheckBox"))
        self.pushButton.setText(_translate("Form", "PushButton"))
        self.checkBox_2.setText(_translate("Form", "CheckBox"))
        self.pushButton_2.setText(_translate("Form", "PushButton"))
        self.checkBox_3.setText(_translate("Form", "CheckBox"))
        self.pushButton_3.setText(_translate("Form", "PushButton"))
        self.checkBox_4.setText(_translate("Form", "CheckBox"))
        self.pushButton_4.setText(_translate("Form", "PushButton"))
        self.checkBox_5.setText(_translate("Form", "CheckBox"))
        self.pushButton_5.setText(_translate("Form", "PushButton"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

