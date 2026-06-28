# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLayout,
    QMainWindow,
    QMenu,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(611, 371)
        MainWindow.setMaximumSize(QSize(16777215, 411))
        self.actionHelp = QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_7 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout_5.addItem(self.verticalSpacer)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")

        self.verticalLayout_5.addWidget(self.label)

        self.whisperComboBox = QComboBox(self.centralwidget)
        self.whisperComboBox.setObjectName("whisperComboBox")

        self.verticalLayout_5.addWidget(self.whisperComboBox)

        self.verticalLayout_7.addLayout(self.verticalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalSpacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.fromComboBox = QComboBox(self.centralwidget)
        self.fromComboBox.setObjectName("fromComboBox")

        self.verticalLayout.addWidget(self.fromComboBox)

        self.horizontalLayout_6.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalSpacer_3 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.toComboBox = QComboBox(self.centralwidget)
        self.toComboBox.setObjectName("toComboBox")

        self.verticalLayout_2.addWidget(self.toComboBox)

        self.horizontalLayout_6.addLayout(self.verticalLayout_2)

        self.verticalLayout_7.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.horizontalLayout_8.setSizeConstraint(
            QLayout.SizeConstraint.SetDefaultConstraint
        )
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName("label_10")

        self.verticalLayout_9.addWidget(self.label_10)

        self.voiceComboBox = QComboBox(self.centralwidget)
        self.voiceComboBox.setObjectName("voiceComboBox")

        self.verticalLayout_9.addWidget(self.voiceComboBox)

        self.horizontalLayout_8.addLayout(self.verticalLayout_9)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.verticalLayout_10.setSizeConstraint(
            QLayout.SizeConstraint.SetDefaultConstraint
        )
        self.verticalSpacer_7 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout_10.addItem(self.verticalSpacer_7)

        self.voicesButton = QPushButton(self.centralwidget)
        self.voicesButton.setObjectName("voicesButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.voicesButton.sizePolicy().hasHeightForWidth())
        self.voicesButton.setSizePolicy(sizePolicy)

        self.verticalLayout_10.addWidget(self.voicesButton)

        self.horizontalLayout_8.addLayout(self.verticalLayout_10)

        self.horizontalLayout_8.setStretch(0, 1)

        self.verticalLayout_7.addLayout(self.horizontalLayout_8)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName("line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_7.addWidget(self.line)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalSpacer_4 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout_3.addItem(self.verticalSpacer_4)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")

        self.verticalLayout_3.addWidget(self.label_7)

        self.inputComboBox = QComboBox(self.centralwidget)
        self.inputComboBox.setObjectName("inputComboBox")

        self.verticalLayout_3.addWidget(self.inputComboBox)

        self.horizontalLayout_7.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalSpacer_5 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout_4.addItem(self.verticalSpacer_5)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName("label_8")

        self.verticalLayout_4.addWidget(self.label_8)

        self.outputComboBox = QComboBox(self.centralwidget)
        self.outputComboBox.setObjectName("outputComboBox")

        self.verticalLayout_4.addWidget(self.outputComboBox)

        self.horizontalLayout_7.addLayout(self.verticalLayout_4)

        self.verticalLayout_7.addLayout(self.horizontalLayout_7)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName("line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_7.addWidget(self.line_2)

        self.warningLabel = QLabel(self.centralwidget)
        self.warningLabel.setObjectName("warningLabel")
        self.warningLabel.setEnabled(True)
        self.warningLabel.setStyleSheet("color: rgb(217, 83, 79);")

        self.verticalLayout_7.addWidget(self.warningLabel)

        self.startButton = QPushButton(self.centralwidget)
        self.startButton.setObjectName("startButton")
        self.startButton.setMinimumSize(QSize(0, 32))

        self.verticalLayout_7.addWidget(self.startButton)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 611, 33))
        self.menubar.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.menubar.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuHelp.setTearOffEnabled(False)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.HelpFaq))
        self.menuHelp.setIcon(icon)
        self.menuTranslation = QMenu(self.menubar)
        self.menuTranslation.setObjectName("menuTranslation")
        icon1 = QIcon(QIcon.fromTheme("accessories-character-map"))
        self.menuTranslation.setIcon(icon1)
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuTranslation.menuAction())
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "BabbleFish", None)
        )
        self.actionHelp.setText(QCoreApplication.translate("MainWindow", "Help", None))
        self.actionAbout.setText(
            QCoreApplication.translate("MainWindow", "About", None)
        )
        self.label.setText(
            QCoreApplication.translate("MainWindow", "Whisper model", None)
        )
        self.label_2.setText(
            QCoreApplication.translate("MainWindow", "Translate from", None)
        )
        self.label_3.setText(
            QCoreApplication.translate("MainWindow", "Translate to", None)
        )
        self.label_10.setText(QCoreApplication.translate("MainWindow", "Voice", None))
        self.voicesButton.setText(
            QCoreApplication.translate("MainWindow", "Get more voices...", None)
        )
        self.label_7.setText(
            QCoreApplication.translate("MainWindow", "Input device", None)
        )
        self.label_8.setText(
            QCoreApplication.translate("MainWindow", "Output device", None)
        )
        self.warningLabel.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )
        self.startButton.setText(
            QCoreApplication.translate("MainWindow", "Start", None)
        )
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", "Help", None))
        self.menuTranslation.setTitle(
            QCoreApplication.translate("MainWindow", "Translation", None)
        )

    # retranslateUi
