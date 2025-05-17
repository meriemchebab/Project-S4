from PySide6 import QtCore, QtGui, QtWidgets
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(817, 588)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 111, 451))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.pushButton_7 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_7.setObjectName("pushButton_7")
        self.verticalLayout.addWidget(self.pushButton_7)
        
        self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)
        
        self.pushButton_4 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        
        self.pushButton_5 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout.addWidget(self.pushButton_5)
        
        self.pushButton_6 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.verticalLayout.addWidget(self.pushButton_6)
        
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        
        self.pushButton_8 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_8.setObjectName("pushButton_8")
        self.verticalLayout.addWidget(self.pushButton_8)
        
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        
        self.tab_3 = QtWidgets.QTabWidget(self.centralwidget)
        self.tab_3.setGeometry(QtCore.QRect(120, 0, 691, 491))
        self.tab_3.setObjectName("tab_3")
        
        # Tab 1
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        
        self.horizontalSlider = QtWidgets.QSlider(self.tab)
        self.horizontalSlider.setGeometry(QtCore.QRect(350, 410, 251, 16))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        
        self.horizontalSlider_2 = QtWidgets.QSlider(self.tab)
        self.horizontalSlider_2.setGeometry(QtCore.QRect(30, 410, 251, 16))
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        
        self.radioButton = QtWidgets.QRadioButton(self.tab)
        self.radioButton.setGeometry(QtCore.QRect(30, 430, 109, 20))
        self.radioButton.setObjectName("radioButton")
        
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(30, 390, 231, 21))
        self.label.setObjectName("label")
        
        self.frame = QtWidgets.QFrame(self.tab)
        self.frame.setGeometry(QtCore.QRect(0, 0, 691, 391))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        
        self.pushButton_11 = QtWidgets.QPushButton(self.frame)
        self.pushButton_11.setGeometry(QtCore.QRect(330, 0, 51, 24))
        self.pushButton_11.setObjectName("pushButton_11")
        
        self.pushButton_12 = QtWidgets.QPushButton(self.frame)
        self.pushButton_12.setGeometry(QtCore.QRect(390, 0, 51, 24))
        self.pushButton_12.setObjectName("pushButton_12")
       
        self.radioButton_3 = QtWidgets.QRadioButton(self.tab)
        self.radioButton_3.setGeometry(QtCore.QRect(350, 430, 109, 20))
        self.radioButton_3.setObjectName("radioButton_3")
        
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(350, 390, 231, 21))
        self.label_2.setObjectName("label_2")
        
        self.tab_3.addTab(self.tab, "")
        
        # Tab 2
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        
        self.frame_2 = QtWidgets.QFrame(self.tab_2)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 691, 391))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        
        self.pushButton_9 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_9.setGeometry(QtCore.QRect(274, 0, 51, 24))
        self.pushButton_9.setObjectName("pushButton_9")
        
        self.pushButton_10 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_10.setGeometry(QtCore.QRect(330, 0, 51, 24))
        self.pushButton_10.setObjectName("pushButton_10")
        
        self.horizontalSlider_3 = QtWidgets.QSlider(self.tab_2)
        self.horizontalSlider_3.setGeometry(QtCore.QRect(30, 410, 251, 16))
        self.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_3.setObjectName("horizontalSlider_3")
        
        self.horizontalSlider_4 = QtWidgets.QSlider(self.tab_2)
        self.horizontalSlider_4.setGeometry(QtCore.QRect(380, 410, 251, 16))
        self.horizontalSlider_4.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_4.setObjectName("horizontalSlider_4")
        
        self.radioButton_2 = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_2.setGeometry(QtCore.QRect(30, 430, 109, 20))
        self.radioButton_2.setObjectName("radioButton_2")
        
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(30, 390, 231, 21))
        self.label_3.setObjectName("label_3")
        
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(380, 390, 231, 21))
        self.label_4.setObjectName("label_4")
        
        self.tab_3.addTab(self.tab_2, "")
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 817, 33))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tab_3.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_7.setText(_translate("MainWindow", "open file"))
        self.comboBox.setItemText(0, _translate("MainWindow", "plot 2D"))
        self.comboBox.setItemText(1, _translate("MainWindow", "both planes"))
        self.comboBox.setItemText(2, _translate("MainWindow", "split planes"))
        self.pushButton_4.setText(_translate("MainWindow", "plot 3D"))
        self.pushButton_5.setText(_translate("MainWindow", "change color 2D"))
        self.pushButton_6.setText(_translate("MainWindow", "change color 3D"))
        self.pushButton.setText(_translate("MainWindow", "online view"))
        self.pushButton_3.setText(_translate("MainWindow", " save project"))
        self.pushButton_8.setText(_translate("MainWindow", "load project"))
        self.pushButton_2.setText(_translate("MainWindow", "read from USB"))
        self.radioButton.setText(_translate("MainWindow", "SHOW Detie"))
        self.label.setText(_translate("MainWindow", "Smooth the plot"))
        self.pushButton_11.setText(_translate("MainWindow", "back"))
        self.pushButton_12.setText(_translate("MainWindow", "next"))
        self.radioButton_3.setText(_translate("MainWindow", "NORMIIZE"))
        self.label_2.setText(_translate("MainWindow", "zoom the plot"))
        self.tab_3.setTabText(self.tab_3.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.pushButton_9.setText(_translate("MainWindow", "back"))
        self.pushButton_10.setText(_translate("MainWindow", "next"))
        self.radioButton_2.setText(_translate("MainWindow", "normelize"))
        self.label_3.setText(_translate("MainWindow", "Smooth the plot"))
        self.label_4.setText(_translate("MainWindow", "zoom the plot"))
        self.tab_3.setTabText(self.tab_3.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
