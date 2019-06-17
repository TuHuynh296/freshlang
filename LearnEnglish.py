import win32com.client as wincl
from SQliteHelper import *
from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia
from MainWindow import Ui_MainWindow
from congratulation import Ui_Congrat
import time
import numpy as np
import sys
import re


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() 
            # ~== super(ApplicationWindow, self).__init__()
            # phải gọi khởi tạo từ lớp cha thì lớp con mới kế thừa được
        self.ui = Ui_MainWindow(self)
            # ui kế thừa từ class này, và class này kế thừa từ QMainWindow 
        self.ui.setupUi(self)
        self.DictDB = SQLiteHelper('DictDB.db')
        self.listen = False
        self.checkSentenceEncore = False
        self.count = 0
        self.acronyms = [["'s ", ' is '], ["'re ", ' are '], ["'m ", ' am '], ["'d ", ' would '], ["'ve ", ' have '], ["'ll ", ' will '], ["can't ", ' can not '], ["don't ", ' do not']]

    # Event key for mainwindow
    # Kế thừa chỉ được thực hiện trong lớp con !!!
    # def keyPressEvent(self, event):
    #     if event.key() == QtCore.Qt.Key_0:
    #         self.close()

    def ChooseIDToLoad(self):
        rowids = self.DictDB.get_rowid_from_sort_score()
        id = -1
        if self.count == 0:
            self.listen = False
            id = rowids[np.random.randint(10)][0]
            self.SetButtonIcon(self.ui.toolButton, 'edit')
            self.ui.addWordButtonToLayoutEng('Result')
            self.ui.toolButton_3.show()  
        elif self.count == 3:
            id = rowids[np.random.randint(10, len(rowids))][0]
            self.listen = True
            self.ui.label.setText('Listen to type ...')
            self.SetButtonIcon(self.ui.toolButton, 'speak')
            self.TextToSpeech(self.DictDB.select_lang_by_rowid('ENG', id))
            self.ui.toolButton_3.hide()
            self.listen = True
            self.count = -1
        else:
            id = rowids[np.random.randint(10, len(rowids))][0]
        self.count +=1
        return int(id)

    def LoadEngSentence(self):
        # rowid là giá trị không bị trùng và ko thay đổi !!!
        index = self.ChooseIDToLoad()
        self.rowid = index
        if not self.listen:
            sentence = self.DictDB.select_lang_by_rowid('VIE', index)
            self.ui.label.setText(sentence)    
        self.ui.addWordButtonToLayoutEng('Result')

        # Tắt phím sửa câu tiếng anh, khi nào enter lineEdit thì mở lại
        self.ui.toolButton_3.setEnabled(False)
        self.ui.toolButton_4.setEnabled(False)

    def ConvertAcronyms(self, sentence):
        for w1, w2 in self.acronyms:
            sentence = sentence.replace(w1, w2)
        return sentence

    
    def FillCharectInSentence(self, sentence):
        sentence = re.sub(r'[^\w\s\']', ' ', sentence)
        sentence = sentence.replace("''", ' ')
        sentence = re.sub(r'\s+', ' ', sentence)
        sentence = re.sub(r'\A\s+|\s+\B', '', sentence) # bỏ đầu bỏ cuối khoảng trắng
        return sentence.lower()

    def FindPosErrorWords(self, s1, s2):
        left, right = -1, -1
        def findPos(start, stop, step):
            for index in range(start, stop, step):
                if s1[index] != s2[index]:
                    return index
            return -1

        left = findPos(0, len(s1), 1)
        right = findPos(-1, -(len(s1)+1), -1)
        return [left, right]
    
    def ChangeColorForWordButton(self, word_buttons, background, color):
        for wb in word_buttons:
            wb.setStyleSheet("background-color: %s; color: %s"%(background, color))

    def PaintColorWordButtons(self, word_buttons, left, right):
        head = word_buttons[:left]
        if right == -1:
            middle = word_buttons[left:]
            tail = []
        else:
            middle = word_buttons[left:right+1]
            tail = word_buttons[right+1:]
        
        self.ChangeColorForWordButton(head, "rgb(255, 255, 255)", "rgb(0, 0, 0)")
        self.ChangeColorForWordButton(middle, "rgb(255, 0, 0)", "rgb(255, 255, 255)")
        self.ChangeColorForWordButton(tail, "rgb(255, 255, 255)", "rgb(0, 0, 0)")

    def setStyleTextHTML(self, text, color = '#000000', size='10', weight = '0', style = 'none', decoration = 'none'):
        text = ("""<p style=" margin-top:0px; 
                    margin-bottom:0px; 
                    margin-left:0px; 
                    margin-right:0px; 
                    -qt-block-indent:0; 
                    text-indent:0px;">
                    <span style=" font-size:%spt; 
                    font-weight:%s; 
                    font-style:%s; 
                    text-decoration: %s; 
                    color:%s;">%s</span></p>"""%(size, weight, style, decoration, color, text))
        return text

    def Reload(self):
        self.count = 0
        self.LoadEngSentence()
        self.ui.progressBar.setFormat('0/20')
        self.ui.numTrueSentence = 0
        self.ui.progressBar.setValue(0)
        self.ui.lineEdit.setText('')
        self.ui.pressEnterTwiceLineEdit = False
        self.ui.text_browser.hide()
        self.EnableWidgetsInLayout(self.ui.hz_image_eng, False)
    
    def GetLang(self, lang):
        return self.DictDB.select_lang_by_rowid(lang, self.rowid)

    def TextToSpeech(self, text):
        text = text.replace('_', ' ')
        speak = wincl.Dispatch("SAPI.SpVoice")
        speak.Speak(text)

    def BellRing(self, type):
        if type == 1:
            self.sound = QtMultimedia.QSound('assets/correct.wav')
        elif type == 2: 
            self.sound = QtMultimedia.QSound('assets/wrong.wav')
        else:
            self.sound = QtMultimedia.QSound('assets/congrat.wav')
        self.sound.play()

    def SetButtonIcon(self, button, name):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/%s.png"%(name)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        button.setIcon(icon)
        button.setIconSize(QtCore.QSize(32,32))

    def deleteWidgetsInLayout(self, layout):
        for i in reversed(range(layout.count())): 
            widgetToRemove = layout.itemAt(i).widget()
            # remove it from the layout list
            layout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)

    def EnableWidgetsInLayout(self, layout, turn):
        for i in reversed(range(layout.count())): 
            widget = layout.itemAt(i).widget()
            if turn:
                widget.show()
            else:
                widget.hide()


# s1 = "satan's mnist".split(' ')
# s2 = "satan's minions".split(' ')
# s1 = 'david hunt detective of metropolitan police'.split(' ')
# s2 = 'detective david hunt of the metropolitan police'.split(' ')

# app = QtWidgets.QApplication(sys.argv)
# appwindow = ApplicationWindow()
# pos = appwindow.FindPosErrorWords(s1,s2)
# appwindow.PaintColorWordButtons(s2, pos[0], pos[1])

app = QtWidgets.QApplication(sys.argv)
appwindow = ApplicationWindow()
    
def main():
    appwindow.LoadEngSentence()
    appwindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

# DictDB = SQLiteHelper('DictDB.db')
# def InitAttDictDB(DictDB):
#     DictDB.create_table("""CREATE TABLE DICTDB( 
#                             ENG TEXT, 
#                             VIE TEXT, 
#                             SCR INTEGER
#                         )""")

# def AddSentenceToDB(DictDB):
#     with open('./assets/studyphim.txt', 'r', encoding = 'utf8') as file:
#         content = file.readlines()

#     for data in content:
#         split_data = data.split('&&&')
#         eng = split_data[0]
#         vie = split_data[1]
#         score = split_data[2].replace(' điểm\n', '')
#         DictDB.edit("INSERT INTO DICTDB (ENG, VIE, SCR) VALUES (\"" + eng + '", "' + vie + '", ' + score + ')')

# InitAttDictDB(DictDB)
# AddSentenceToDB(DictDB)

# Lỗi QLayout: Attempting to add QLayout "" to QMainWindow "Form", which already has a layout
# Khắc phục:
# không nên kế thừa từ QMainWindow và QWidget tại một thời điểm vì QMainWindow thừa hưởng từ QWidget, không cần thiết 

# Một tùy chọn khác là triển khai một lớp kế thừa từ QWidget, không phải từ QMainWindow.