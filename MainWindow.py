# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!
from threading import Thread
import threading
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
from dialog import *    
from congratulation import *
from VideoShow import *
import re
from bs4 import BeautifulSoup
import requests
import urllib
import functools
import random
from selenium_scrapping import Scraping


# central widget sẽ là tham chiếu của tất cả các thành phần trong mainwindow
# vertical layout sẽ add các layout con khác
# các layout con khác sẽ add các widget trong nó như (button, label...)

class Ui_MainWindow(object):

    def __init__(self, parent = None):
        self.parent = parent
        self.pressEnterTwiceLineEdit = False
        self.uiDialog = Ui_Dialog(self) # từ dialog
        self.word_buttons = []
        # tham chiếu parent để truyền qua lại dữ liệu
        #self.uiDialog.setupUi(self.window) # kế thừa từ QDialog
            # na ná như bên lớp applycation trong learnenglish.py
        self.translated_word = ''
        self.scraping = Scraping(0)    
        self.st2_waiting = False
        
    def newKeyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            self.google_trans(self.lineEdit.text(), 'e2v')
            self.getImageForWord(self.lineEdit.text())            

        if event.key() == Qt.Key_A:
            self.google_trans(self.lineEdit.text(), 'v2e')
            self.getImageForWord(self.lineEdit.text())

        if event.key() == Qt.Key_W and self.toolButton_trans2.isEnabled():
            self.google_trans(self.parent.GetLang('ENG'), 'e2v')
            self.getImageForWord(self.parent.GetLang('ENG'))
        
        if event.key() == Qt.Key_S:
            if self.pressEnterTwiceLineEdit or self.parent.listen:
                self.parent.TextToSpeech(self.parent.GetLang('ENG'))

        if event.key() == Qt.Key_D and self.parent.s2t and not self.st2_waiting:
            self.speak()


    def OpenVideo(self):
        self.uiVideo = VideoShow(self)
        self.uiVideo.show()

    def OpenCongrat(self):
        self.congratwindow = Congrat_Window(self)
        self.congratwindow.show()

    def OpenWindow(self, lang):
        def open():
            if self.parent.listen:
                self.parent.TextToSpeech(self.parent.GetLang('ENG'))
            else:
                if lang == 'VIE':
                    self.uiDialog.lineEdit.setText(self.parent.GetLang('VIE'))
                    self.uiDialog.lang_selected = 'VIE'
                else:
                    self.uiDialog.lineEdit.setText(self.parent.GetLang('ENG'))
                    self.uiDialog.lang_selected = 'ENG'

                    # gán text của lable vào text của textEdit để chỉnh sửa !!!
                # Giữ label hiện tại để thay đổi trong dialog
                self.uiDialog.show()
                # sau khi khởi tạo đối tượng QMainWindow() là một dialog, ta sẽ show nó 
        return open
            # dùng hàm open lồng trong OpenWindow để mục đích cuối cùng là trả về địa chỉ hàm
                # hợp lệ cho event
            # Nếu không dùng hàm lồng nhau trả về địa chỉ hàm nó sẽ ngầm hiểu label là kiểu bool và ko có thuộc tính text !!!
    

    def addWordButtonToLayoutEng(self, text):
        text = re.sub(r"[^\w\-']", ' ', text).strip()
        text = re.sub(r'\s+', ' ', text)
        layout = self.hz_vocabulary_eng
        # del widgets from hz_vocabulary_eng
        self.parent.deleteWidgetsInLayout(layout)
        self.word_buttons = []

        # add widgets to hz_vocabulary_eng
        list_word = text.split(' ')
        for i, word in enumerate(list_word):
            word_button = QtWidgets.QPushButton(self.centralwidget)
            word_button.setObjectName('word_button%s'%i)
            # fix callable objects in loop
            slot = functools.partial(self.translate, word)
            word_button.clicked.connect(slot)
            self.word_buttons.append(word_button)
            word_button.setText(word)
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setFamily("Time News Roman")
            word_button.setFont(font)
            layout.addWidget(word_button)

    def google_trans(self, sentence, mode):
        self.translated_word = ''
        if sentence.replace(' ', '') == '':
            return 
        trsl, spelling, word_type_and_content, hint = self.scraping.google_translate(sentence, mode)
        self.text_browser.clear()
        self.text_browser.show()
        self.text_browser.append(self.parent.setStyleTextHTML(trsl, color= '#005500', size = '14'))
        if hint:
            self.text_browser.append(self.parent.setStyleTextHTML(hint, color= '#ff0000', size = '10'))
        if spelling:
            self.text_browser.append(self.parent.setStyleTextHTML(spelling, color= '#ffaa00', size = '10'))
        if word_type_and_content[0] and word_type_and_content[1]:
            viet_word = True
            for line in word_type_and_content[1]:
                if line in word_type_and_content[0]:
                    self.text_browser.append(self.parent.setStyleTextHTML(line, color= '#005500', size = '12', weight= '500'))
                elif viet_word:
                    self.text_browser.append(self.parent.setStyleTextHTML(line, color= '#5500ff', size = '10', style= 'italic'))
                    viet_word = False
                else:
                    self.text_browser.append(self.parent.setStyleTextHTML(line, color= '#000000', size = '10'))
                    viet_word = True
        self.text_browser.moveCursor(QtGui.QTextCursor.Start)

    def speak(self):
        self.lineEdit.setText('')
        self.lineEdit.setPlaceholderText('Speech to text >>> Listening ... <<<')
        self.scraping.speech_to_text(self)
        
    def translate(self, word):
        # show text_browser and hz_image_eng
        if self.translated_word == word:
            self.getImageForWord(word)
            return

        self.translated_word = word
        self.text_browser.show()
        self.parent.EnableWidgetsInLayout(self.hz_image_eng, True)
        self.getImageForWord(word)
        self.text_browser.clear()
        word = re.sub(r"[^-'\w]", ' ', word).lower()
        word = word.replace('_', '-')
        if word == '':
            return
        page = requests.get("https://dict.laban.vn/find?type=1&query=%s"%(word))
        soup = BeautifulSoup(page.content, 'html.parser')
        spelling = soup.find('h2', {'class':'fl'}).text
        content = soup.find('div',{'id':'content_selectable', 'class':'content'})
        if content == None:
            return
        word_type = content.find_all('div', {'class':'bg-grey bold font-large m-top20'})
        word_type = [wt.find('span').text for wt in word_type]
        content = [w.replace('\xa0', ' ') for w in content.text.split('\n')][1:len(content)-1]
        self.text_browser.append(self.parent.setStyleTextHTML(word, color= '#005500', size = '17'))
        self.text_browser.append(self.parent.setStyleTextHTML(spelling))
        for i, wt in enumerate(word_type):
            self.text_browser.append(self.parent.addTagScroll(wt, 'href', '#', i, 8, 'underline', '0000ff'))
        text = ''
        count = 0
        for line in content:
            if line in word_type:
                self.text_browser.append(self.parent.addTagScroll('\n' + line, 'name', '', count, 14, 'none', 'ffaa00'))
                count+=1
            else:
                temp = word[:int(len(word)/2)]
                temp = word if len(temp)<=2 else temp
                if line.lower().find(temp)!=-1:
                    text = self.parent.setStyleTextHTML(line, color= '#aa55ff', style='italic', weight = '600')
                else:
                    text = self.parent.setStyleTextHTML(line)
                self.text_browser.append(text)

        self.text_browser.moveCursor(QtGui.QTextCursor.Start)

    def getImageForWord(self, word):
        try:
            self.parent.deleteWidgetsInLayout(self.hz_image_eng)
            page = requests.get("https://vn.images.search.yahoo.com/search/images?fr=sfp&p=" + word + "&fr2=p%3As%2Cv%3Ai&.bcrumb=uKIyJ5aGvwE&save=0")
            soup = BeautifulSoup(page.content, 'html.parser')
            images = soup.find_all('img')
            images = [img.attrs['src'] for img in images if 'src' in img.attrs]
            if len(images)<4:
                max = len(images)
            else:
                max = 4

            for _ in range(max):
                i = random.randint(0,len(images)-1)
                data = urllib.request.urlopen(images[i]).read()
                image = QtGui.QImage()
                image.loadFromData(data)
                lbl = QtWidgets.QLabel(self.centralwidget)
                lbl.setPixmap(QtGui.QPixmap(image).scaled(200,200))
                #lbl.setFixedSize(QtCore.QSize(200,200))
                self.hz_image_eng.addWidget(lbl)
                del images[i]
        except:
            pass


    def show(self, result):
        self.toolButton_3.setEnabled(True)
        self.toolButton_4.setEnabled(True)
        self.toolButton_trans2.setEnabled(True)

        self.pressEnterTwiceLineEdit = True


        # so khớp 2 kết quả
        # sửa sai lần hai cho các từ giống như như 's ~ is, 're ~ are ...
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

            self.addWordButtonToLayoutEng(result)
            if self.numTrueSentence == 20:
                self.OpenCongrat()
                self.parent.BellRing(3)
        else:
            if not self.parent.checkSentenceEncore:
                self.parent.checkSentenceEncore = True
                self.show(result)
                return
            self.parent.BellRing(2)
            if not self.parent.s2t:
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
            self.addWordButtonToLayoutEng(result)
            self.parent.PaintColorWordButtons(self.word_buttons, pos[0], pos[1])
            self.parent.checkSentenceEncore = False

    def showResult(self):
        # Không show result nếu chưa nhập gì cả hoặc chỉ toàn là khoảng trắng
        string = self.lineEdit.text().replace(' ', '')

        if not self.pressEnterTwiceLineEdit: # lần enter thứ nhất
            if string == '': # chuỗi rỗng
                QtWidgets.QMessageBox.information(None, 'WARNING', 'Please type corectly english translation !!!')
            else:
                if self.parent.listen:
                    self.label.setText(self.parent.GetLang('VIE'))
                    self.parent.SetButtonIcon(self.toolButton, 'edit')
                    self.parent.listen = False
                    self.toolButton_3.show()
                result = self.parent.GetLang('ENG')
                # Thread(target= self.show(result)).start()
                # Thread(target= self.parent.TextToSpeech(result)).start()
                self.show(result)
                self.parent.TextToSpeech(result)
        else: # lần enter thứ 2
                if self.parent.s2t:
                    self.lineEdit.setPlaceholderText('Type english translation')
                    self.parent.s2t = False
                self.pressEnterTwiceLineEdit = False
                self.lineEdit.setText('')
                self.parent.EnableWidgetsInLayout(self.hz_image_eng, False)
                self.text_browser.hide()
                self.parent.LoadEngSentence()
                self.parallel_s2t_threading()
                # self.label_2.setStyleSheet('color: black;')    

    def parallel_s2t_threading(self):
        # self.worker = Worker()
        self.thread = QThread(self.parent)
        self.thread.started.connect(self.speech2text_shot) # <--new line, make sure work starts.
        self.thread.start()

    def speech2text_shot(self):
        if np.random.randint(3) == 0 and self.parent.firstStart:
            self.lineEdit.setReadOnly(True)
            self.parent.s2t = True
            self.speak()
        else:
            self.lineEdit.setReadOnly(False)

    def DeleteCouple(self, MainWindow):
        def delete():
            reply = QtWidgets.QMessageBox.question(MainWindow, 'Message', "Do you want to delete this couple?", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                self.parent.DictDB.deleteById(self.parent.rowid)     
                self.parent.LoadEngSentence()                 
        return delete


    def setupUi(self, MainWindow):
        MainWindow.keyPressEvent = self.newKeyPressEvent      
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

        self.text_browser = QtWidgets.QTextBrowser(self.centralwidget)
        self.text_browser.hide()
        self.verticalLayout.addWidget(self.text_browser)
        # self.text_browser.setText('ok baby\nyou are the one for me\n')
        # self.text_browser.setHtml("""My image :<br /><p style="text-align:center;"><img src="assets/enter.png" height="100" width="100"/>
        #                             <img src="assets/speak.png" height="100" width="100"/>
        #                             """)
        # self.text_browser.setFixedHeight(250)


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
        self.toolButton.setIconSize(QtCore.QSize(20,20))
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.toolButton)

        # Truyền tham số vào hàm sự kiện !!!
        # Vì sự kiện cần một địa chỉ hàm ko phải là hàm thực thi
        # nên sẽ dùng hàm lồng nhau 
        self.toolButton.clicked.connect(self.OpenWindow('VIE'))

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        # self.lineEdit.keyPressEvent = self.newKeyPressEvent
        # self.lineEdit.keyReleaseEvent = self.newKeyReleaseEvent

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
        self.toolButton_2.setIconSize(QtCore.QSize(20,20))
        self.toolButton_2.setObjectName("toolButton_2")
        icon_trans = QtGui.QIcon()
        icon_trans.addPixmap(QtGui.QPixmap("assets/google_translate_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.toolButton_trans = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_trans.setIcon(icon_trans)
        self.toolButton_trans.setIconSize(QtCore.QSize(20,20))
        self.toolButton_trans.setObjectName('toolButton_trans')
        self.toolButton_trans.clicked.connect(lambda: self.google_trans(self.lineEdit.text(), 'e2v'))
        
        self.verLayA = QtWidgets.QVBoxLayout()
        self.verLayA.setObjectName('verLayA')
        self.verLayA.addWidget(self.toolButton_2)
        self.verLayA.addWidget(self.toolButton_trans)

        self.horizontalLayout_2.addLayout(self.verLayA)

        #Event toolButton_2
        self.toolButton_2.clicked.connect(self.showResult)


        # ProgressBar
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        # set text progressbar
        self.numTrueSentence = 0
        self.progressBar.setTextVisible(True)
        self.progressBar.setFormat('0/20')
        

        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("assets/speak.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        self.toolButton_3 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_3.setIcon(icon3)
        self.toolButton_3.setIconSize(QtCore.QSize(20,20))
        self.toolButton_3.setObjectName("toolButton_3")

        self.verticalLayout_2.addWidget(self.toolButton_3)

        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("assets/edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.toolButton_4 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_4.setIcon(icon4)
        self.toolButton_4.setIconSize(QtCore.QSize(20,20))
        self.toolButton_4.setObjectName('toolButton_4')

        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("assets/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_5 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_5.setIcon(icon5)
        self.toolButton_5.setIconSize(QtCore.QSize(16,16))
        self.toolButton_5.setObjectName('toolButton_5')
        self.toolButton_5.clicked.connect(self.DeleteCouple(MainWindow))
        self.toolButton_4.clicked.connect(self.OpenWindow('ENG'))

        self.toolButton_trans2 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_trans2.setIcon(icon_trans)
        self.toolButton_trans2.setIconSize(QtCore.QSize(20,20))
        self.toolButton_trans2.setObjectName('toolButton_trans2')
        self.toolButton_trans2.clicked.connect(lambda: self.google_trans(self.parent.GetLang('ENG'), 'e2v'))

        self.verticalLayout_2.addWidget(self.toolButton_4)
        self.verticalLayout_2.addWidget(self.toolButton_trans2)
        self.verticalLayout_2.setAlignment(Qt.AlignRight)

        self.hz_vocabulary_eng = QtWidgets.QHBoxLayout()
        self.hz_vocabulary_eng.setObjectName('horizontalLayout_eng')
        self.hz_vocabulary_eng.setAlignment(Qt.AlignLeft)

        self.horizontalLayout_3.addLayout(self.hz_vocabulary_eng)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.hz_image_eng = QtWidgets.QHBoxLayout()
        self.hz_image_eng.setObjectName('horizontalLayoutImageEng')
        self.verticalLayout.addLayout(self.hz_image_eng)
        self.verticalLayout.addWidget(self.progressBar)
        self.verticalLayout.addWidget(self.toolButton_5)

        self.toolButton_3.clicked.connect(lambda: self.parent.TextToSpeech(self.parent.GetLang('ENG')))

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
        self.toolButton_3.setText(_translate("MainWindow", "Edit result"))
        self.menuFile.setTitle(_translate("MainWindow", "Option"))
        self.actionReload.setText(_translate("MainWindow", "Reload"))
        self.actionSave_sentence_source.setText(_translate("MainWindow", "Save sentence source"))
        self.actionVideo.setText(_translate("MainWindow", "Learn with Video"))