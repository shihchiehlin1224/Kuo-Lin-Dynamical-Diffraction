# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'error_message.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class input_alert(QtWidgets.QDialog):

    def __init__(self):
        super(input_alert, self).__init__()
        self.init_ui()

    def init_ui(self):
        
        self.resize(300, 120)
        self.setMinimumSize(QtCore.QSize(330, 120))
        self.setMaximumSize(QtCore.QSize(400, 120))
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel(self)
        self.verticalLayout.addWidget(self.label)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        # self.show()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; color:#fc0107;\">INPUT INCOMPLETE!!</span></p><p align=\"center\"><span style=\" font-size:18pt; color:#fc0107;\">PLEASE CHECK</span></p></body></html>"))
    
    def new_content(self, comment, color):
        _translate = QtCore.QCoreApplication.translate
        new_string = "<html><head/><body>"
        for item in comment:
            new_string  += "<p align=\"center\"><span style=\" font-size:18pt; color:%s;\">%s</span></p>" %(color, item)
        new_string += "</body></html>"
        self.label.setText(_translate("Dialog", new_string))    

