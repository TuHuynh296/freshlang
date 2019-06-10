# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!
from threading import Thread
from PyQt5 import QtCore, QtGui, QtWidgets
from dialog import *
from congratulation import *
from VideoShow import *
import re

# central widget sẽ là tham chiếu của tất cả các thành phần trong mainwindow
# vertical layout sẽ add các layout con khác
# các layout con khác sẽ add các widget trong nó như (button, label...)

class Ui_MainWindow(object):

    def __init__(self, parent = None):
        self.parent = parent
        self.pressEnterTwiceLineEdit = False
        self.uiDialog = Ui_Dialog(self) # từ dialog
        # tham chiếu parent để truyền qua lại dữ liệu
        #self.uiDialog.setupUi(self.window) # kế thừa từ QDialog
            # na ná như bên lớp applycation trong learnenglish.py

    def OpenVideo(self):
        self.uiVideo = VideoShow(self)
        self.uiVideo.show()

    def OpenCongrat(self):
        self.congratwindow = Congrat_Window(self)
        self.congratwindow.show()

    def OpenWindow(self, label):
        def open():
            if self.parent.listen:
                self.parent.TextToSpeech(self.parent.DictDB.select_lang_by_rowid('ENG', self.parent.rowid))
            else:
                if label == self.label:
                    self.uiDialog.lineEdit.setText(label.text())
                else:
                    result = self.parent.DictDB.select_lang_by_rowid('ENG', self.parent.rowid)
                    self.uiDialog.lineEdit.setText(result)
                    # gán text của lable vào text của textEdit để chỉnh sửa !!!
                # Giữ label hiện tại để thay đổi trong dialog
                self.currentLabel = label
                self.uiDialog.show()
                # sau khi khởi tạo đối tượng QMainWindow() là một dialog, ta sẽ show nó 
        return open
            # dùng hàm open lồng trong OpenWindow để mục đích cuối cùng là trả về địa chỉ hàm
                # hợp lệ cho event
            # Nếu không dùng hàm lồng nhau trả về địa chỉ hàm nó sẽ ngầm hiểu label là kiểu bool và ko có thuộc tính text !!!
            
    def show(self, result):
        self.toolButton_3.setEnabled(True)
        self.toolButton_4.setEnabled(True)
        self.pressEnterTwiceLineEdit = True

        # so khớp 2 kết quả
        # sửa sai lần hai cho các từ giống như như 's ~ is, 're ~ are
        if self.parent.checkSentenceEncore:
            s1 = self.parent.ConvertAcronyms(result)
            s2 = self.parent.ConvertAcronyms(self.lineEdit.text())
            s1 = self.parent.FillCharectInSentence(s1)
            s2 = self.parent.FillCharectInSentence(s2)
        else:
            s1 = self.parent.FillCharectInSentence(result)
            s2 = self.parent.FillCharectInSentence(self.lineEdit.text())
        if s1 == s2:
            self.parent.BellRing(1)
            if self.numTrueSentence >= 0:
                self.progressBar.setProperty('value', self.progressBar.value() + 5)
            self.parent.DictDB.update_score(self.parent.DictDB.get_score(result) + 1, result)
            self.numTrueSentence+=1
            self.progressBar.setFormat('%s/20'%(str(self.numTrueSentence)))
            self.label_2.setText(result)
            self.label_2.setStyleSheet('color: blue;')
            if self.numTrueSentence == 20:
                self.OpenCongrat()
                self.parent.BellRing(3)
        else:
            if not self.parent.checkSentenceEncore:
                self.parent.checkSentenceEncore = True
                self.show(result)
                return
            self.parent.BellRing(2)
            self.progressBar.setProperty('value', self.progressBar.value() - 5)
            self.parent.DictDB.update_score(self.parent.DictDB.get_score(result) - 1, result)
            self.numTrueSentence-=1
            self.progressBar.setFormat('%s/20'%(str(self.numTrueSentence)))
            s1 = self.lineEdit.text().split(' ')
            s2 = self.parent.FillCharectInSentence(result).split(' ')
            pos = [-1,-1]
            if len(s1) <= len(s2):
                pos = self.parent.FindPosErrorWords(s1, s2)
            else:
                pos = self.parent.FindPosErrorWords(s2, s1)
            self.label_2.setText(self.parent.PaintColorForSentence(result.split(' '), pos[0], pos[1]))
            self.parent.checkSentenceEncore = False
            #self.label_2.setStyleSheet('color: orange;')

    def showResult(self):
        # Không show result nếu chưa nhập gì cả hoặc chỉ toàn là khoảng trắng
        string = self.lineEdit.text().replace(' ', '')

        if not self.pressEnterTwiceLineEdit: # lần enter thứ nhất
            if string == '': # chuỗi rỗng
                QtWidgets.QMessageBox.information(None, 'WARNING', 'Please type corectly english translation !!!')
            else:
                if self.parent.listen == True:
                    self.label.setText(self.parent.DictDB.select_lang_by_rowid('VIE', self.parent.rowid))
                    self.parent.SetButtonIcon(self.toolButton, 'edit')
                    self.parent.listen = False
                    self.toolButton_3.show()
                result = self.parent.GetEngResult()
                # Thread(target= self.show(result)).start()
                # Thread(target= self.parent.TextToSpeech(result)).start()
                self.show(result)
                self.parent.TextToSpeech(result)
        else:
                self.parent.LoadEngSentence()
                self.pressEnterTwiceLineEdit = False
                self.lineEdit.setText('')
                self.label_2.setStyleSheet('color: black;')    

    def DeleteCouple(self, MainWindow):
        def delete():
            reply = QtWidgets.QMessageBox.question(MainWindow, 'Message', "Do you want to delete this couple?", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                self.parent.DictDB.deleteById(self.parent.rowid)     
                self.parent.LoadEngSentence()
                          
        return delete
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(603, 318)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        # tạo layout chứa label và button
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName('horizontalLayout')

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName('horizontalLayout_2')

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName('horizontalLayout_3')

        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName('verticalLayout_2')


        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setWordWrap(True)
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        fontLabel1 = QtGui.QFont()
        fontLabel1.setPointSize(14)
        fontLabel1.setBold(True)

        fontLabel2 = QtGui.QFont()
        fontLabel2.setPointSize(14)
        fontLabel2.setBold(True)

        fontLineEdit = QtGui.QFont()
        fontLineEdit.setFamily("Times New Roman")
        fontLineEdit.setPointSize(16)
        fontLineEdit.setBold(True)
        fontLineEdit.setItalic(False)
        fontLineEdit.setWeight(75)

        self.label.setFont(fontLabel1)
        self.label.setObjectName("label")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QtCore.QSize(32,32))
        self.toolButton.setObjectName("toolButton")

        self.horizontalLayout.addWidget(self.toolButton)

        # Truyền tham số vào hàm sự kiện !!!
        # Vì sự kiện cần một địa chỉ hàm ko phải là hàm thực thi
        # nên sẽ dùng hàm lồng nhau 
        self.toolButton.clicked.connect(self.OpenWindow(self.label))

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.lineEdit.setFont(fontLineEdit)
        self.lineEdit.setAutoFillBackground(False)
        self.lineEdit.setText('')
        self.lineEdit.setDragEnabled(False)
        self.lineEdit.setClearButtonEnabled(False)
        self.lineEdit.setStyleSheet("color: green;")

        self.lineEdit.setObjectName("lineEdit")
        # ẩn chữ trong lineEdit
        self.lineEdit.setPlaceholderText('Type english translation')

        # Event lineEdit
        self.lineEdit.returnPressed.connect(self.showResult)

        # Hiện con trỏ văn bản khi mở app 
        self.lineEdit.setFocus(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("assets/enter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.toolButton_2 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_2.setIcon(icon2)
        self.toolButton_2.setIconSize(QtCore.QSize(32,32))
        self.toolButton_2.setObjectName("toolButton_2")
        self.horizontalLayout_2.addWidget(self.toolButton_2)

        #Event toolButton_2
        self.toolButton_2.clicked.connect(self.showResult)

        # self.work = Worker()
        # self.thread = QThread()
        # self.thread.started.connect(self.worker.work) # <--new line, make sure work starts.
        # self.thread.start()

        # ProgressBar
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)

        # set text progressbar
        self.numTrueSentence = 0
        self.progressBar.setTextVisible(True)
        self.progressBar.setFormat('0/20')
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setFont(fontLabel2)
        self.label_2.setObjectName("label_2")
        self.label_2.setWordWrap(True)

        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("assets/speak.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        self.toolButton_3 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_3.setIcon(icon3)
        self.toolButton_3.setIconSize(QtCore.QSize(32,32))
        self.toolButton_3.setObjectName("toolButton_3")

        self.verticalLayout_2.addWidget(self.toolButton_3)

        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("assets/edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.toolButton_4 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_4.setIcon(icon4)
        self.toolButton_4.setIconSize(QtCore.QSize(32,32))
        self.toolButton_4.setObjectName('toolButton_4')

        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("assets/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_5 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_5.setIcon(icon5)
        self.toolButton_5.setIconSize(QtCore.QSize(16,16))
        self.toolButton_5.setObjectName('toolButton_5')
        self.toolButton_5.clicked.connect(self.DeleteCouple(MainWindow))
        self.verticalLayout.addWidget(self.toolButton_5)


        self.toolButton_4.clicked.connect(self.OpenWindow(self.label_2))

        self.verticalLayout_2.addWidget(self.toolButton_4)
        self.horizontalLayout_3.addWidget(self.label_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.toolButton_3.clicked.connect(lambda: self.parent.TextToSpeech(self.parent.GetEngResult()))

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 603, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.actionReload = QtWidgets.QAction(MainWindow)
        self.actionReload.setObjectName("actionReload")
        self.actionSave_sentence_source = QtWidgets.QAction(MainWindow)
        self.actionSave_sentence_source.setObjectName("actionSave_sentence_source")
        self.menuFile.addAction(self.actionReload)

        # event actionReload
        self.actionReload.triggered.connect(self.parent.Reload)

        self.menuFile.addAction(self.actionSave_sentence_source)
        self.menubar.addAction(self.menuFile.menuAction())

        # Menu video
        self.actionVideo = QtWidgets.QAction(MainWindow)
        self.actionVideo.setObjectName('actionVideo')
        self.menubar.addAction(self.actionVideo)
        self.actionVideo.triggered.connect(self.OpenVideo)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "STUDY ENGLISH"))
        self.label.setText(_translate("MainWindow", "Vietnamese Sentence"))
        self.toolButton.setText(_translate("MainWindow", "Edit Sentence"))
        self.toolButton_2.setText(_translate("MainWindow", "Check"))
        self.label_2.setText(_translate("MainWindow", "Result"))
        self.toolButton_3.setText(_translate("MainWindow", "Edit result"))
        self.menuFile.setTitle(_translate("MainWindow", "Option"))
        self.actionReload.setText(_translate("MainWindow", "Reload"))
        self.actionSave_sentence_source.setText(_translate("MainWindow", "Save sentence source"))
        self.actionVideo.setText(_translate("MainWindow", "Learn with Video"))



# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
