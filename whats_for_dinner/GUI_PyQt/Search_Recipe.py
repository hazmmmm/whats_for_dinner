from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import (
    QDialog,
    QApplication,
    QFileDialog,
    QMessageBox,
    QMainWindow,
    QPushButton,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
)
from PyQt6.QtGui import QPixmap
from PyQt6.uic import loadUi
import os
from os.path import dirname, realpath, join
import sys
import pandas as pd


class Recipe(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_Search_Recipe()
        self.ui.setupUi(self)
        self.setWindowTitle("Recipe")  # Window title
        self.ui.Browse.clicked.connect(self.browsefiles)
        self.ui.add.clicked.connect(self.start)

    def browsefiles(self):
        global path_to_image
        fname = QFileDialog.getOpenFileName(
            self, "Open File", ".//files//apple.jpg"
        )  # "Images (*.png, *.jpg)
        self.ui.lineEdit_recipe.setText(fname[0])
        path_to_image = fname[0]

    def p_t_i(self):
        return path_to_image

    def start(self):
        file_name, file_extension = os.path.splitext(self.ui.lineEdit_recipe.text())

        if (
            file_extension == ".jpg"
            or file_extension == ".jpeg"
            or file_extension == ".png"
        ):
            self.ui.openWindow()

        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("ERROR")
            dlg.setText(
                f"Please select 🚀jpg, 🚀jpeg, or 🚀png files! NOT: 👉{file_extension}👈 file!"
            )
            dlg.setIcon(QMessageBox.Icon.Warning)
            dlg.setStyleSheet("background-color: rgb(180, 3, 3);")
            button = dlg.exec()
            QMessageBox.StandardButton.Ok


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1200, 1266)
        Form.setStyleSheet("")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 0, 1, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.spinBox = QtWidgets.QSpinBox(self.tab)
        self.spinBox.setGeometry(QtCore.QRect(78, 9, 45, 27))
        self.spinBox.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.UpArrowCursor))
        self.spinBox.setMouseTracking(True)
        self.spinBox.setObjectName("spinBox")

        self.spinBox.setValue(5)

        self.BtnDescribe = QtWidgets.QPushButton(self.tab)
        self.BtnDescribe.setGeometry(QtCore.QRect(129, 11, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.BtnDescribe.setFont(font)
        self.BtnDescribe.setObjectName("BtnDescribe")
        self.label_Column_count = QtWidgets.QLabel(self.tab)
        self.label_Column_count.setGeometry(QtCore.QRect(9, 9, 63, 21))
        self.label_Column_count.setObjectName("label_Column_count")
        self.tableWidget_CSV = QtWidgets.QTableWidget(self.tab)
        self.tableWidget_CSV.setGeometry(QtCore.QRect(0, 750, 1171, 461))
        self.tableWidget_CSV.setMinimumSize(QtCore.QSize(1171, 461))
        self.tableWidget_CSV.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.CursorShape.SizeAllCursor)
        )
        self.tableWidget_CSV.setMouseTracking(True)
        self.tableWidget_CSV.setObjectName("tableWidget_CSV")
        self.tableWidget_CSV.setColumnCount(0)
        self.tableWidget_CSV.setRowCount(0)
        self.label_IMG = QtWidgets.QLabel(self.tab)
        self.label_IMG.setGeometry(QtCore.QRect(0, 30, 1171, 671))
        self.label_IMG.setMinimumSize(QtCore.QSize(1171, 671))
        self.label_IMG.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor))
        self.label_IMG.setMouseTracking(True)
        self.label_IMG.setText("")
        self.label_IMG.setScaledContents(True)
        self.label_IMG.setObjectName("label_IMG")
        self.progressBar = QtWidgets.QProgressBar(self.tab)
        self.progressBar.setGeometry(QtCore.QRect(0, 712, 1171, 31))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.tabWidget.addTab(self.tab, "")
        self.gridLayout.addWidget(self.tabWidget, 2, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

        recipe = Recipe()
        self.pixmap = QPixmap(recipe.p_t_i())
        self.label_IMG.setPixmap(self.pixmap)
        self.CSV()

        self.BtnDescribe.clicked.connect(self.CSV)

    def CSV(self):
        self.path = "../../raw_data/food_dot_com/recipes_cleaned.csv"
        self.all_data = pd.read_csv(self.path)

        numColomn = self.spinBox.value()
        if numColomn == 0:
            NumRows = len(self.all_data.index)
        else:
            NumRows = numColomn
        self.tableWidget_CSV.setColumnCount(len(self.all_data.columns))
        self.tableWidget_CSV.setRowCount(NumRows)
        self.tableWidget_CSV.setHorizontalHeaderLabels(self.all_data.columns)

        for i in range(NumRows):
            for j in range(len(self.all_data.columns)):
                self.tableWidget_CSV.setItem(
                    i, j, QTableWidgetItem(str(self.all_data.iat[i, j]))
                )

        self.tableWidget_CSV.resizeColumnsToContents()
        self.tableWidget_CSV.resizeRowsToContents()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.BtnDescribe.setText(_translate("Form", "Describe"))
        self.label_Column_count.setText(_translate("Form", "Columns"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab), _translate("Form", "Describe data")
        )


class Ui_Search_Recipe(QMainWindow, Ui_Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def openWindow(self):
        self.window = QtWidgets.QWidget()
        self.ui2 = Ui_Form()
        self.ui2.setupUi(self.window)
        self.window.show()

    def setupUi(self, Search_Recipe):
        Search_Recipe.setObjectName("Search_Recipe")
        Search_Recipe.resize(989, 797)
        Search_Recipe.setAutoFillBackground(False)
        Search_Recipe.setStyleSheet("background-color: rgb(248, 245, 223)")
        self.gridLayout = QtWidgets.QGridLayout(Search_Recipe)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(Search_Recipe)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.recipe_label = QtWidgets.QLabel(self.frame)
        self.recipe_label.setText("")
        self.recipe_label.setPixmap(QtGui.QPixmap("img/Main_Picture.png"))
        self.recipe_label.setScaledContents(True)
        self.recipe_label.setObjectName("recipe_label")
        self.gridLayout_2.addWidget(self.recipe_label, 0, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lineEdit_recipe = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_recipe.setStyleSheet(
            "background-color: rgb(255, 255, 255);\n" 'font: 75 16pt "MS Shell Dlg 2";'
        )
        self.lineEdit_recipe.setInputMask("")
        self.lineEdit_recipe.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.lineEdit_recipe.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_recipe.setDragEnabled(True)
        self.lineEdit_recipe.setAcceptDrops(True)
        self.lineEdit_recipe.setPlaceholderText("Please select picture")
        self.lineEdit_recipe.setClearButtonEnabled(True)
        self.lineEdit_recipe.setObjectName("lineEdit_recipe")
        self.gridLayout_3.addWidget(self.lineEdit_recipe, 0, 0, 1, 1)
        self.add = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Yellowtail")
        font.setPointSize(22)
        font.setUnderline(True)
        font.setStrikeOut(False)
        self.add.setFont(font)
        self.add.setMouseTracking(True)
        self.add.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.add.setCheckable(False)
        self.add.setObjectName("add")
        self.gridLayout_3.addWidget(self.add, 1, 0, 1, 2)
        self.Browse = QtWidgets.QPushButton(self.frame_2)
        self.Browse.setMinimumSize(QtCore.QSize(0, 27))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.Browse.setFont(font)
        self.Browse.setMouseTracking(True)
        self.Browse.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Browse.setCheckable(False)
        self.Browse.setAcceptDrops(True)
        self.Browse.setObjectName("Browse")
        self.gridLayout_3.addWidget(self.Browse, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.frame_2, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(Search_Recipe)
        QtCore.QMetaObject.connectSlotsByName(Search_Recipe)

    def retranslateUi(self, Search_Recipe):
        _translate = QtCore.QCoreApplication.translate
        Search_Recipe.setWindowTitle(_translate("Search_Recipe", "Form"))
        self.lineEdit_recipe.setText(
            _translate(
                "Search_Recipe", "Please select picture (.jpg or .jpeg or .png) "
            )
        )
        self.add.setText(_translate("Search_Recipe", "Search Recipe"))
        self.Browse.setText(_translate("Search_Recipe", "     Browse    "))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.cursorFlashTime()
    widget = Recipe()
    widget.setWindowIcon(QtGui.QIcon(".//img//logo.ico"))
    widget.show()
    app.exec()
