# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VideoShow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDir, QUrl, Qt, QThread, QSizeF, QSize, QRectF
from PyQt5.QtWidgets import QWidget, QFileDialog, QSlider, QGraphicsScene, QGraphicsView
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaObject
from PyQt5.QtMultimediaWidgets import QVideoWidget, QGraphicsVideoItem
from win32api import GetSystemMetrics
from Slider import *
import pysrt
import time
class VideoShow(QtWidgets.QWidget):
    
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.start()
        #self.turnOnOrOffButton(False)

    def start(self):
        self.toolButton.setEnabled(False)
        self.startTimeSubsInScroll = dict()
        self.listStartTime = []
        self.indexNextSub = 0
        self.isEnableSub = False
        self.isEnableSub2 = False
        self.isOpenedVideo = False
        self.isEngOrVieOrTwiceSubLabel = 3
        self.buttonCtrlPressed = False

    # Tắt focus để bắt sự kiện button arrow !!!
    def setChildrenFocusPolicy (self, policy):
        def recursiveSetChildFocusPolicy (parentQWidget):
            for childQWidget in parentQWidget.findChildren(QWidget):
                childQWidget.setFocusPolicy(policy)
                recursiveSetChildFocusPolicy(childQWidget)
        recursiveSetChildFocusPolicy(self)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.buttonCtrlPressed = False

    def keyPressEvent(self, event):
        print(self.buttonCtrlPressed)

        if event.key() == Qt.Key_Control:
            self.buttonCtrlPressed = True
        #print(self.isFullScreen())
        if event.key() == Qt.Key_Escape and self.isFullScreen():
            self.fullScreen()

        if event.key() == Qt.Key_Enter:
            if self.frameSlider.isHidden():
                self.frameSlider.show()
                self.frameButton.show()
            else:
                self.frameSlider.hide()
                self.frameButton.hide()

        if event.key() == Qt.Key_Space:
            self.play()
        
        if event.key() == Qt.Key_Right:
            self.forwardVideo()

        if event.key() == Qt.Key_Left:
            self.backwardVideo()

        if event.key() == Qt.Key_Comma:
            self.backwarSub()

        if event.key() == Qt.Key_Period:
            self.forwardSub()
        
        if event.key() == Qt.Key_E:
            self.isEngOrVieOrTwiceSubLabel = 1
            self.setLabelVieo(1)

        if event.key() == Qt.Key_V:
            self.isEngOrVieOrTwiceSubLabel = 2
            self.setLabelVieo(2)

        if event.key() == Qt.Key_T:
            self.isEngOrVieOrTwiceSubLabel = 3
            self.setLabelVieo(3)
        
        if event.key() == Qt.Key_S and not self.buttonCtrlPressed: # sử dụng thêm keyReleaseEvent để đánh dấu nút ctrl
            if self.labelVideo.isVisible():
                self.labelVideo.setVisible(False)
            else:
                self.labelVideo.setVisible(True)

        if event.key() == Qt.Key_F:
            self.fullScreen()
        
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier and Qt.Key_S:
            self.saveCoupleFromButtonEvent()
            
        # mouseMouve Event
    # def mouseMoveEvent(self, event):
    #     if self.frameSlider.isHidden():
    #         self.frameSlider.show()
    #         print('show frameslider')
    #         QThread.sleep(3)
    #         self.frameSlider.hide()
    #         print('hide frameslider')    

    def setLabelVieo(self, typeof):
        if self.labelVideo.text() != '':
            if self.indexNextSub != 0 or self.indexNextSub != len(self.listStartTime) - 1:
                text = self.listStartTime[self.indexNextSub-1][0].text()
            else:
                text = self.listStartTime[self.indexNextSub][0].text()
            if typeof == 1 and self.isEnableSub:
                self.labelVideo.setText(text.split('\n')[0])
            elif typeof ==2 and self.isEnableSub2:
                self.labelVideo.setText(text.split('\n')[1])
            elif self.isEnableSub and self.isEnableSub2:
                self.labelVideo.setText(text)


    def turnOnOrOffSubVideoLabel(self):
        if self.labelVideo.isVisible():
            self.labelVideo.setVisible(False)
        else:
            self.labelVideo.setVisible(True)

    def forwardVideo(self):
        pos = self.mediaPlayer.position()
        if self.isEnableSub:
            if self.indexNextSub >=1:
                self.indexNextSub-=1
            self.grabIndexCurrent(pos + 10000, len(self.listStartTime)-1, 1)
        self.mediaPlayer.setPosition(pos+ 10000)

    def backwardVideo(self):
        pos = self.mediaPlayer.position()
        if self.isEnableSub:
            if self.indexNextSub < len(self.listStartTime)-1:
                self.indexNextSub+=1
            if pos > self.maxTimeVideo:
                pos = self.maxTimeVideo
            self.grabIndexCurrent(pos - 10000, 0, -1)
        self.mediaPlayer.setPosition(pos- 10000)

    def forwardSub(self):
        if self.isEnableSub:
            self.mediaPlayer.setPosition(self.listStartTime[self.indexNextSub][2])
            self.setStatusScrollArea()

    def backwarSub(self):
        if self.isEnableSub and self.indexNextSub >= 2:
            self.indexNextSub -=2
            self.mediaPlayer.setPosition(self.listStartTime[self.indexNextSub][2])
            self.setStatusScrollArea()


    def calculateTime(self, subRipTime):
        time = str(subRipTime).replace(',', ':')
        time = time.split(':')
        time = list(map(lambda x: int(x), time))
        time = (time[0]*3600 + time[1]*60 + time[2])*1000 + time[3]
        return time

    def saveCoupleFromButtonEvent(self):
        if self.isEnableSub and self.isEnableSub2:
            checkbox = None
            if self.indexNextSub !=0:
                checkbox = self.listStartTime[self.indexNextSub-1][0]
            else:
                checkbox = self.listStartTime[self.indexNextSub][0]
            if checkbox.isChecked():
                checkbox.setChecked(False)
            else:
                checkbox.setChecked(True)
            self.saveCouple(checkbox)

    def saveCouple(self, checkbox):
        if self.isEnableSub and not self.actionOpenSub2.isEnabled():
            text = checkbox.text()
            if text.find('\n') == -1:
                checkbox.setEnabled(False)
                QtWidgets.QMessageBox.information(None, 'WARNING', "Can't save with single sentence")
                return
            couple = text.split('\n')
            print(checkbox.isChecked())
            if not checkbox.isChecked():
                self.parent.parent.DictDB.delete('ENG', couple[0])
                QtWidgets.QMessageBox.information(None, 'Notification', 'Couple was deleted !')
            else:
                result1 = self.parent.parent.DictDB.selectRowIDByEngOrVie('ENG', couple[0])
                result2 = self.parent.parent.DictDB.selectRowIDByEngOrVie('VIE', couple[1])
                if len(result1) == 0 and len(result2) == 0:
                    self.parent.parent.DictDB.insert(couple[0], couple[1], 0)
                    QtWidgets.QMessageBox.information(None, 'Notification', 'Couple was inserted !')
                else:
                    QtWidgets.QMessageBox.information(None, 'WARNING', 'Couple already exist in revision')
            self.buttonCtrlPressed = False
    def eventSubCheckBox(self, checkbox):
        def event():
            self.saveCouple(checkbox)
        return event
    
    def eventSubButton(self, time, index):
        # time tính theo milisecond
        def event():
            self.mediaPlayer.setPosition(time)
            self.indexNextSub = index
            self.setStatusScrollArea()
        return event

    def enableCheckBoxsOrButtonScroll(self, index):
        if self.isEnableSub:
            for item in self.listStartTime:
                item[index].setEnabled(True)
    

    
    def loadSubToScroll(self, fileName):
        subs = pysrt.open(fileName)
        for index, value in enumerate(subs):
            horizontalLayoutScroll = QtWidgets.QHBoxLayout()
            checkbox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
            checkbox.setObjectName('checkbox%s'%(index))
            text = value.text.replace('\n', ' ').replace("\"", "''")
            checkbox.setText(text.replace('\xa0', ' '))
            checkbox.setFixedHeight(50)
            checkbox.setFont(QtGui.QFont('Times New Roman', 10))
            checkbox.clicked.connect(self.eventSubCheckBox(checkbox))
            checkbox.setFocusPolicy(Qt.NoFocus)
            button = QtWidgets.QToolButton(self.scrollAreaWidgetContents)
            button.setObjectName('button%s'%(index))
            button.setFixedHeight(20)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("assets/access.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            button.setIcon(icon)
            button.setIconSize(QtCore.QSize(32, 32))
            button.setFocusPolicy(Qt.NoFocus)
            checkbox.setEnabled(False)
            if not self.isOpenedVideo:
                button.setEnabled(False)

            startTime = self.calculateTime(value.start)
            endTime = self.calculateTime(value.end)
            button.clicked.connect(self.eventSubButton(startTime, index))
            horizontalLayoutScroll.addWidget(checkbox,0)
            horizontalLayoutScroll.addWidget(button,10)
            horizontalLayoutScroll.setContentsMargins(0, 0, 50, 0)  # left, top, right, bottom
            self.verticalScroll.addLayout(horizontalLayoutScroll)
            self.startTimeSubsInScroll[str(startTime)] = index
            self.listStartTime.append([checkbox, button, startTime, endTime, value.start])

    def LoadOtherSub(self, fileName):
        subs = pysrt.open(fileName)
        if subs[5].start == self.listStartTime[5][2] and subs[10].end == self.listStartTime[10][3]:
            for index, item in enumerate(self.listStartTime):
                while subs[0].start < item[4]:
                    del subs[0]
                if subs[0].start == item[4]:
                    text = subs[0].text.replace('\n', ' ').replace('\xa0', ' ').replace("\"", "''")
                    item[0].setText(item[0].text()+'\n'+ text)
                    del subs[0]
                    
            self.actionOpenSub2.setEnabled(False)
            self.enableCheckBoxsOrButtonScroll(0)
            self.isEnableSub2 = True
        else:
            QtWidgets.QMessageBox.information(None, 'WARNING', 'Please choose correctly sub compatible with engsub')

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            self.mediaPlayer.stop()
        else:
            event.ignore()

    def reloadVideoAndSub(self):
        self.clearLayout(self.verticalScroll)
        #self.mediaPlayer.setMedia(QMediaPlayer.NoMedia)
        #self.mediaPlayer.destroyed()
        QMediaPlayer.stop(self.mediaPlayer)
        # init
        self.start()

        self.scrollArea.hide()
        self.actionOpenSub1.setEnabled(True)
        self.actionOpenSub2.setEnabled(False)
        print(len(self.listStartTime))
    
    def turnOnOrOffButton(self, turn):
        buttons = [self.toolButton, self.toolButton_3, self.toolButton_4]
        map(lambda x: x.setEnabled(turn), buttons)

    def openFile(self, title):
        def open():
            choose = -1
            dialog = QtWidgets.QFileDialog()
            extension = ''
            if title == 'Open Video':
                extension = 'Videos (*.mkv *.mp4 *.mpg)'
                choose = 1
            elif title == 'Open Eng Sub':
                extension = 'SRT (*.srt)'
                choose = 2
            else:
                extension = 'SRT (*.srt)'
                choose = 3
            #dialog.setDefaultSuffix(".srt")
            fileName, _ = dialog.getOpenFileName(None, title, QDir.homePath(), extension)
            name = fileName.lower()
            if choose == 2: # quy ước loại sub sẽ đặt tên ở đuôi !!!
                if name[len(name)-7:len(name)-4] != 'eng':
                    QtWidgets.QMessageBox.information(None, 'WARNING', 'Please choose correctly sub with format *eng.srt')
                    return
            elif choose == 3:
                if name[len(name)-7:len(name)-4] != 'vie':
                    QtWidgets.QMessageBox.information(None, 'WARNING', 'Please choose correctly sub with format *vie.srt')
                    return

            if fileName != '':
                #self.loadSubToScroll()
                if title == 'Open Video':
                    self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
                    self.toolButton.setEnabled(True)
                    self.enableCheckBoxsOrButtonScroll(1)
                    self.isOpenedVideo = True
                    #self.turnOnOrOffButton(True)
                    self.play()
                elif title == 'Open Eng Sub':
                    self.loadSubToScroll(fileName)
                    self.scrollArea.show()
                    self.isEnableSub = True
                    self.actionOpenSub2.setEnabled(True)
                    self.actionOpenSub1.setEnabled(False)
                else:
                    self.LoadOtherSub(fileName)
        return open

    def play(self):
        icon = QtGui.QIcon()
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            icon.addPixmap(QtGui.QPixmap("assets/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.toolButton.setIcon(icon)
        else:
            icon.addPixmap(QtGui.QPixmap("assets/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.toolButton.setIcon(icon)
            self.mediaPlayer.play()

    def scrollToSub(self, curHeight, maxHeight):
        # dùng hệ thức chéo để tính tỉ lệ !
        self.maxButtonPos = self.listStartTime[-1][1].y()
        pos = int(float(curHeight/self.maxButtonPos)*maxHeight)
        #print(pos, curHeight, maxHeight)
        self.scrollArea.verticalScrollBar().setValue(pos)
        
    # hàm sự kiện này có đối số position là mặc định !!!

    def setTextCheckBox(self, checkbox, color, size, italic_):
        checkbox.setStyleSheet('color: %s'%(color))
        checkbox.setFont(QtGui.QFont('Times New Roman', size, italic = italic_))

    def setStatusScrollArea(self):
        timeSub = self.listStartTime[self.indexNextSub]
        self.setTextCheckBox(timeSub[0], 'green', 15, True)
        if self.oldIndexSub != 0:
            self.setTextCheckBox(self.listStartTime[self.oldIndexSub][0], 'black', 10, False)
            self.scrollToSub(timeSub[1].y(), self.scrollArea.verticalScrollBar().maximum())
            text = timeSub[0].text()
            if self.isEngOrVieOrTwiceSubLabel == 1:
                self.labelVideo.setText(text.split('\n')[0])
            elif self.isEngOrVieOrTwiceSubLabel == 2:
                self.labelVideo.setText(text.split('\n')[1])
            else:
                self.labelVideo.setText(text)
        self.oldIndexSub = self.indexNextSub
        if self.indexNextSub < len(self.listStartTime)-1:
            self.indexNextSub +=1


    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        self.labelCurTime.setText(self.formatTimeToHMS(position))
        if self.isEnableSub:
            start = self.listStartTime[self.indexNextSub][2]
            end = self.listStartTime[self.indexNextSub][3]
            if position >= start and position <= end:
                self.setStatusScrollArea()

    def grabIndexCurrent(self, position, stopIndex, step):
        indexCur = self.indexNextSub
        for i in range(indexCur, stopIndex, step):
            start = self.listStartTime[i][2]
            end = self.listStartTime[i][3]
            if position >= start and position <= end:
                self.indexNextSub = i
                break
            if step == 1 and position >= end and position <= self.listStartTime[i+1][2]:
                self.indexNextSub = i +1
                break
            elif step == -1 and position <= start and position >= self.listStartTime[i-1][2]:
                self.indexNextSub = i
                break

        if indexCur == self.indexNextSub:
            if step == 1:
                self.indexNextSub = len(self.listStartTime) -1
            else:
                self.indexNextSub = 1
        #print(self.indexNextSub)

    def formatTime(self, time):
        if len(time) == 1:
            return '0' + time
        return time

    def formatTimeToHMS(self, time):
        time = time/1000
        hour = int(time/3600)
        minute = int((time-3600*hour)/60)
        second = int(time-3600*hour - minute*60)
        return '%s:%s:%s'%(self.formatTime(str(hour)), self.formatTime(str(minute)), self.formatTime(str(second)))
        
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        self.maxTimeVideo = duration
        self.labelDurationTime.setText(self.formatTimeToHMS(duration))

    # sliderMoved có sẵn tham số position cho slider để tùy chỉnh video !!!
    def sliderMoved(self, position):
        self.mediaPlayer.setPosition(position)        

    def setSCrollbar(self, number): 
        def setScroll():
            #self.scrollArea.scrollContentsBy(0, number)
            #self.scrollAreaWidgetContents.scroll(number)
            vbar = self.scrollArea.verticalScrollBar()
            #print(vbar.maximum())
            vbar.setValue(number)
            
        return setScroll

    def fullScreen(self):
        icon = QtGui.QIcon()
        if self.isFullScreen():
            icon.addPixmap(QtGui.QPixmap("assets/fullscreen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.toolButtonFullScreen.setIcon(icon)
            self.verticalLayout.setContentsMargins(9,9,9,9)
            if self.isEnableSub:
                self.scrollArea.show()
            self.menubar.show()
            self.frameSlider.show()
            self.frameButton.show()
            self.showNormal()
            self.videoItem.setSize(QSizeF(600, 400))
            #self.graphicsView.fitInView(QRectF(-400, -400, 400, 400), Qt.KeepAspectRatio)
            #self.graphicsView.setMaximumSize(QSize(600, 400))
            #self.graphicsView.setAlignment(Qt.AlignCenter)
            self.labelVideo.hide()
        else:
            icon.addPixmap(QtGui.QPixmap("assets/minimize.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.toolButtonFullScreen.setIcon(icon)
            self.verticalLayout.setContentsMargins(0,0,0,0)
            if self.isEnableSub:
                self.scrollArea.hide()
            self.menubar.hide()
            self.frameSlider.hide()
            self.frameButton.hide()
            self.showFullScreen()
            self.videoItem.setSize(QSizeF(self.width()-1, self.height()-2))
            self.labelVideo.show()

    def setupUi(self, Form):
        self.sizeMonitor = [GetSystemMetrics(0), GetSystemMetrics(1)]
        self.setMouseTracking(True)
        self.form = Form
        Form.setObjectName("Form")
        Form.resize(631, 406)

        self.oldHighLine = None
        self.oldIndexSub = 0
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.positionChanged.connect(self.positionChanged) # bắt frame video thay đổi
        self.mediaPlayer.durationChanged.connect(self.durationChanged) # bắt thời lượng video 
            # Hàm này chỉ chạy có 1 lần !!!

        # Create Slider tạo thanh trượt video
        #self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider = Slider(Qt.Horizontal) 
            # truyền đối số Qt.Horizontal không dùng hàm __init__ nó sẽ kế thừa trực tiếp từ Horizontal
            # nếu dùng hàm __init__ nó sẽ ko kế thừa được mà chỉ tham chiếu đến lớp horizontal !!!
        self.positionSlider.parent = self
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.sliderMoved)

        # set event notify 500 millisecond
        QMediaObject.setNotifyInterval(self.mediaPlayer, 500)

        # Create Menubar
        self.menubar = QtWidgets.QMenuBar(Form)
        self.menubar.setFixedHeight(25)
        
        self.menuOpen = QtWidgets.QMenu(self.menubar)
        self.menuOpen.setObjectName('menuOpen')

        self.menuOption = QtWidgets.QMenu(self.menubar)
        self.menuOption.setObjectName('menuOption')
        self.actionReload = QtWidgets.QAction(Form)
        self.actionReload.setObjectName('actionReload')
        self.actionReload.triggered.connect(self.reloadVideoAndSub)
        self.menuOption.addAction(self.actionReload)

        self.actionOpenVideo = QtWidgets.QAction(Form)
        self.actionOpenVideo.setObjectName('openvideo')
        self.actionOpenSub1 = QtWidgets.QAction(Form)
        self.actionOpenSub1.setObjectName('openSub1')
        self.actionOpenSub1.triggered.connect(self.openFile('Open Eng Sub'))
        self.actionOpenSub2 = QtWidgets.QAction(Form)
        self.actionOpenSub2.setObjectName('openSub2')
        self.actionOpenSub2.triggered.connect(self.openFile('Open Vie Sub'))
        self.menuOpen.addAction(self.actionOpenVideo)
        self.menuOpen.addAction(self.actionOpenSub1)
        self.menuOpen.addAction(self.actionOpenSub2)
        self.actionOpenVideo.triggered.connect(self.openFile('Open Video'))
        self.menubar.addAction(self.menuOpen.menuAction())
        self.menubar.addAction(self.menuOption.menuAction())
        self.actionOpenSub2.setEnabled(False)

        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        # create gridlayout contain scrollarea
        # self.gridLayout = QtWidgets.QGridLayout(Form)
        # self.gridLayout.setObjectName("gridLayout")


        # create scrollarea
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMinimumSize(300,400)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 430, 319))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # create verticalscroll
        # chú ý lớp cha là scroll widget content
        self.verticalScroll = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        # self.gridLayout.addWidget(self.scrollArea)

        self.verticalLayout.addWidget(self.menubar, 0)

        scene = QGraphicsScene(self)
        self.graphicsView = QGraphicsView(scene) # dùng widget graphicsview mới overlay lable lên được !!!
        self.videoItem = QGraphicsVideoItem()
        self.videoItem.setSize(QSizeF(600,400))
        #self.graphicsView.setStyleSheet("background-color:black;")
        # dùng palette (bảng màu) riêng cho widget nên không ảnh hưởng đến labelvideo khi ghi đè lên
        p = self.graphicsView.palette()
        p.setColor(self.graphicsView.backgroundRole(), Qt.black)
        self.graphicsView.setPalette(p)
        scene.addItem(self.videoItem)
        self.horizontalLayout.addWidget(self.graphicsView)
        self.mediaPlayer.setVideoOutput(self.videoItem)
        
        # add label for videowidget represent subtitle
        self.labelVideo = QtWidgets.QLabel(self.graphicsView)
        self.labelVideo.setObjectName('labelVideo')
        self.labelVideo.setText('')
        self.labelVideo.setStyleSheet("QLabel {font-size: 20px; opacity:1; color:white}")
        self.labelVideo.setFixedWidth(500)
        self.labelVideo.setFixedHeight(200)
        self.labelVideo.setAlignment(Qt.AlignCenter)
        self.labelVideo.setWordWrap(True)
        self.labelVideo.move(int(self.sizeMonitor[0]/2-200), int(self.sizeMonitor[1]*5/7))
        #print(self.labelVideo.x(), self.labelVideo.y())
        #self.labelVideo.raise_()
        #self.videoWidget.raise_()
        

        self.horizontalLayout.addWidget(self.scrollArea)
        self.verticalLayout.addLayout(self.horizontalLayout,10)
            # cho stretch widget là 100% tức sẽ chiếm toàn bộ diện tích trong layout !!!
            # những widget khác cho 0% stretch

        # create layoutSlider 
        self.horizontalLayoutSlider = QtWidgets.QHBoxLayout()
        self.horizontalLayoutSlider.setObjectName("horizontalLayoutSlider")
        self.labelCurTime = QtWidgets.QLabel(Form)
        self.labelCurTime.setObjectName('labelCurTime')
        self.labelCurTime.setText('00:00')
        self.labelDurationTime = QtWidgets.QLabel(Form)
        self.labelDurationTime.setText('NaN')
        self.labelDurationTime.setObjectName('labelDurationTime')
        self.horizontalLayoutSlider.addWidget(self.labelCurTime)
        self.horizontalLayoutSlider.addWidget(self.positionSlider)
        self.horizontalLayoutSlider.addWidget(self.labelDurationTime)
        #self.verticalLayout.addLayout(self.horizontalLayoutSlider,0)
        # Layout không thể hide được nên sẽ dùng frame (kế thừa từ widget) setlayout để hide nó
        self.frameSlider = QtWidgets.QFrame()
        self.frameSlider.setLayout(self.horizontalLayoutSlider)
        self.verticalLayout.addWidget(self.frameSlider, 0)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        #self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.toolButton = QtWidgets.QToolButton(Form)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QtCore.QSize(32, 32))
        self.toolButton.setObjectName("toolButton")

        # Event play
        self.toolButton.clicked.connect(self.play)

        self.horizontalLayout_2.addWidget(self.toolButton)
        self.toolButton_3 = QtWidgets.QToolButton(Form)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("assets/previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_3.setIcon(icon1)
        self.toolButton_3.setIconSize(QtCore.QSize(32, 32))
        self.toolButton_3.setObjectName("toolButton_3")
        self.toolButton_3.clicked.connect(self.backwardVideo)
        self.horizontalLayout_2.addWidget(self.toolButton_3)
        self.toolButton_4 = QtWidgets.QToolButton(Form)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("assets/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_4.setIcon(icon2)
        self.toolButton_4.setIconSize(QtCore.QSize(32, 32))
        self.toolButton_4.setObjectName("toolButton_4")
        self.toolButton_4.clicked.connect(self.forwardVideo)
        self.horizontalLayout_2.addWidget(self.toolButton_4)
        #self.verticalLayout.addLayout(self.horizontalLayout_2,0)

        self.toolButtonFullScreen = QtWidgets.QToolButton(Form)
        self.toolButtonFullScreen.setObjectName('toolButtonFullScreen')
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap('assets/fullscreen.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonFullScreen.setIcon(icon3)
        self.toolButtonFullScreen.setIconSize(QtCore.QSize(32,32))
        self.horizontalLayout_2.addWidget(self.toolButtonFullScreen)
        self.toolButtonFullScreen.clicked.connect(self.fullScreen)

        # self.toolButton_3.clicked.connect(self.setSCrollbar(30))
        # self.toolButton_4.clicked.connect(self.setSCrollbar(90))
        self.frameButton = QtWidgets.QFrame()
        self.frameButton.setLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.frameButton, 0)

        # turn on mousemove tracking for videowidget !!!
        #self.videoWidget.setMouseTracking(True)

        # tắt mục tiêu tập trung để nhật sự kiện arrow button
        self.setChildrenFocusPolicy(Qt.NoFocus)
        self.scrollArea.setFocusPolicy(Qt.NoFocus)
        # setcontentsmargins cho verticalLayout Tổng chứ ko phải cho Form !!!
        #self.verticalLayout.setContentsMargins(0,0,0,0)

        self.scrollArea.hide()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Study Film"))
        self.toolButton.setText(_translate("Form", "..."))
        self.toolButton_3.setText(_translate("Form", "..."))
        self.toolButton_4.setText(_translate("Form", "..."))
        self.menuOpen.setTitle(_translate("Form", "Open"))
        self.menuOption.setTitle(_translate("Form", "Option"))
        self.actionReload.setText(_translate("Form", 'Reload'))
        self.actionOpenVideo.setText(_translate("Form", 'Open video'))
        self.actionOpenSub1.setText(_translate("Form", 'Open Eng Sub'))
        self.actionOpenSub2.setText(_translate("Form", 'Open Vie Sub'))


