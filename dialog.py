# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        #self.setupUi(QtWidgets.QDialog())

    def editDataBase(self, Dialog):
        def edit():
            if self.parent.label == self.parent.currentLabel:
                self.parent.parent.DictDB.update_lang('VIE', self.lineEdit.text(), self.parent.label.text())
                self.parent.label.setText(self.lineEdit.text())
                Dialog.close()
            else:
                eng = self.parent.parent.DictDB.select_lang_by_rowid('ENG', self.parent.parent.rowid)
                self.parent.parent.DictDB.update_lang('ENG', self.lineEdit.text(), eng)
                #self.parent.label_2.setText(self.lineEdit.text())
                Dialog.close()
        return edit

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)

        # Event returnPress lineEdit
        self.lineEdit.returnPressed.connect(self.editDataBase(Dialog))

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.editDataBase(Dialog))
        self.buttonBox.rejected.connect(lambda: Dialog.close())
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

