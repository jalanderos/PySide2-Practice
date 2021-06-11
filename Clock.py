from PySide2.QtWidgets import QApplication, QWidget, QStyle, QLCDNumber
import sys
from PySide2.QtGui import QIcon, QGuiApplication
from PySide2.QtCore import Qt, QTime, QTimer, SIGNAL


class ParentWidget(QWidget):  # Parent class to allow lower classes to inherit methods
    def __init__(self):
        super().__init__()

    def set_icon(self):  # sets icon for upper left corner of window and pop ups [Add Icon tut]
        app_icon = QIcon("Photos/MrO.jpg")
        self.setWindowIcon(app_icon)

    def init_ui(self, title, width, height):  # initializes UI and makes __init__ in child classes cleaner
        self.setWindowTitle(title)
        self.resize(width, height)
        # centers Window [Center Window tut]
        center = QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, self.size(),
                                    QGuiApplication.primaryScreen().availableGeometry())
        self.setGeometry(center)
        self.set_icon()
        # created obj timer of class QTimer
        # Held here b/c DigitalClock init_ui requires super().init_ui() to create timer first


class DigitalClock(QLCDNumber, ParentWidget):  # Creates class DigitalClock inheriting from QLCDNumber
    # [Digital Clock tut]
    def __init__(self):  # initializes an obj of class DigitalClock when 'obj = DigitalClock()' called
        super().__init__()  # super(ClassName, self) needed when parent requires type(t) as arg 1
        # parent arg needed when inherited class requires, removed from tut code
        self.init_ui("Time", 250, 100)

    def init_ui(self, title, width, height):
        super().init_ui(title, width, height)
        timer = QTimer(self)
        self.connect(timer, SIGNAL('timeout()'), self.show_time)  # Two lines update clock as time goes on
        timer.start(1000)
        self.show_time()  # shows time instantly, avoids 0 on timer when created

    def show_time(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm')
        if (time.second() % 2) == 0:  # if seconds divisible by 2, colon disappears
            text = text[:2] + ' ' + text[3:]  # Gives blinking effect each second
        self.display(text)


if __name__ == '__main__':
    myApp = QApplication(sys.argv)
    clock = DigitalClock()
    clock.show()

    sys.exit(myApp.exec_())
