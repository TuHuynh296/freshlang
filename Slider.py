from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt

class Slider(QSlider):
    # def __init__(self, args, parent = None):
    #     super().__init__()
    #     self.parent = parent
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            e.accept()
            x = e.pos().x()
            value = (self.maximum() - self.minimum()) * x / self.width() + self.minimum()
            self.setValue(value)
            self.parent.labelCurTime.setText(self.parent.formatTimeToHMS(value))
            pos = self.parent.mediaPlayer.position()
            if value > pos:
                self.parent.grabIndexCurrent(value, len(self.parent.listStartTime)-1, 1)
            else:
                self.parent.grabIndexCurrent(value, 0, -1)
            self.parent.mediaPlayer.setPosition(value)
            self.parent.labelVideo.setText('')
        else:
            return super().mousePressEvent(self, e)