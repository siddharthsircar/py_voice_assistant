# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'jarvis2_0.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(487, 467)
        Form.setMinimumSize(QtCore.QSize(487, 467))
        Form.setMaximumSize(QtCore.QSize(487, 467))
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 0, 487, 467))
        self.label.setMinimumSize(QtCore.QSize(487, 467))
        self.label.setMaximumSize(QtCore.QSize(487, 467))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../../resources/ai_animation_1.gif"))
        self.label.setScaledContents(False)
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "J.A.R.V.I.S"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
