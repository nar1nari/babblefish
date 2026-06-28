# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'help.ui'
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
    QLabel,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Ui_HelpWindow(object):
    def setupUi(self, HelpWindow):
        if not HelpWindow.objectName():
            HelpWindow.setObjectName("HelpWindow")
        HelpWindow.resize(717, 453)
        self.verticalLayout = QVBoxLayout(HelpWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QScrollArea(HelpWindow)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 683, 745))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName("label")
        self.label.setTextFormat(Qt.TextFormat.MarkdownText)
        self.label.setScaledContents(False)
        self.label.setWordWrap(True)
        self.label.setOpenExternalLinks(True)

        self.verticalLayout_2.addWidget(self.label)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(HelpWindow)

        QMetaObject.connectSlotsByName(HelpWindow)

    # setupUi

    def retranslateUi(self, HelpWindow):
        HelpWindow.setWindowTitle(
            QCoreApplication.translate("HelpWindow", "About", None)
        )
        self.label.setText(
            QCoreApplication.translate(
                "HelpWindow",
                "# BabbleFish\n"
                "\n"
                "BabbleFish is a real-time speech translation app. It recognizes speech from a microphone, translates it into the selected language, and produces the result using speech synthesis.\n"
                "\n"
                "---\n"
                "\n"
                "# How BabbleFish Works\n"
                "\n"
                "The speech processing process consists of three sequential stages:\n"
                "\n"
                "### 1. Speech Recognition\n"
                "\n"
                "BabbleFish uses the **Whisper** model to convert speech to text.\n"
                "\n"
                "Before launching, you must select a Whisper model.\n"
                "\n"
                "* **Small models** are faster and require less video memory (VRAM), but provide less accurate recognition.\n"
                "* **Large models** significantly improve recognition quality, especially in the presence of noise or accents, but require more VRAM and are slower on low-end graphics cards.\n"
                "\n"
                "### 2. Text Translation\n"
                "\n"
                "After recognition, the text is automatically translated into the selected language.\n"
                "\n"
                "Before launching, specify:\n"
                "\n"
                "* source language;\n"
                "* translation language.\n"
                "\n"
                "### 3. Speec"
                "h translation\n"
                "\n"
                "The translated text is converted to speech and played back through the selected output device.\n"
                "\n"
                "To use speech synthesis, you must first install voice models. This can be done using the **Get more voices...** button.\n"
                "\n"
                "---\n"
                "\n"
                "# Using in voice chats\n"
                "\n"
                "BabbleFish does not automatically create a virtual microphone.\n"
                "\n"
                "If you want to use translation during calls, streams, or voice recordings, you must install a program that emulates a virtual audio device.\n"
                "\n"
                "The simplest and most popular option is using [**VB-CABLE**](https://vb-audio.com/Cable/).\n"
                "\n"
                "## Setup\n"
                "\n"
                "1. Connect your physical microphone as the **Input Device** in BabbleFish.\n"
                "2. Select **VB-CABLE Input** as the **Output Device**.\n"
                "3. In the program where you want to use translation (Discord, Zoom, OBS, games, etc.), select **VB-CABLE Output** as the microphone.\n"
                "\n"
                "After this, your interlocutors will hear the automatically translated and voiced speech, not your origina"
                "l voice.\n"
                "",
                None,
            )
        )

    # retranslateUi
