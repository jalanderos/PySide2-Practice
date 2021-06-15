from PySide2.QtWidgets import QApplication, QWidget, QLabel, QToolTip, QPushButton,\
    QMessageBox, QStyle, QMainWindow, QStatusBar, QProgressBar, QHBoxLayout, QVBoxLayout, \
    QComboBox, QStackedLayout, QRadioButton
import sys
from PySide2.QtGui import QIcon, QFont, QGuiApplication
from PySide2.QtCore import Qt, QTimer, Signal


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


class Window(ParentWidget):  # Creates class Window inheriting from QWidget [First Window tut]
    def __init__(self):  # initializes an obj of class Window
        super().__init__()  # calls init of parent QWidget
        self.classic_names = ["Chris Bumstead", "Terrence Ruffin"]
        self.open_names = ["Mamdouh Elssbiay", "Brandon Curry"]
        self.init_ui("Classic Mr. Olympia", 1200, 400)

    def init_ui(self, title, width, height):
        super().init_ui(title, width, height)
        QToolTip.setFont(QFont("Decorative", 10, QFont.Bold))  # Font for hovering over image msgs
        # Creates overall layout
        outer_box = QVBoxLayout()  # Outer Layout contains stack of upper boxes and lower box
        self.lower_box = QHBoxLayout()  # Contains about, judge buttons, and competitors combobox
        self.set_about()
        self.set_category()
        self.set_competitors()
        self.set_judge()

        self.classic_stack = QStackedLayout()  # Contains Classic competitor pages
        self.classic_stack.addWidget(self.set_page("Photos/CBum.PNG"))  # Add pages To Classic Stack
        self.classic_stack.addWidget(self.set_page("Photos/Terrence.PNG"))
        classic = QWidget()
        classic.setLayout(self.classic_stack)

        self.open_stack = QStackedLayout()  # Contains Open competitor pages
        self.open_stack.addWidget(self.set_page("Photos/Ramy.PNG"))  # Add pages To Open Stack
        self.open_stack.addWidget(self.set_page("Photos/Curry.PNG"))
        open_ = QWidget()
        open_.setLayout(self.open_stack)

        self.category_stack = QStackedLayout()  # Contains Classic and Open category stacks
        self.category_stack.addWidget(classic)
        self.category_stack.addWidget(open_)

        outer_box.addLayout(self.category_stack)  # Outer layout compiled
        outer_box.addLayout(self.lower_box)
        self.setLayout(outer_box)

    def set_page(self, competitor):
        page = QWidget()
        self.upper_box = QHBoxLayout()  # Contains three filtered pictures of competitor
        self.set_icon_modes(competitor)  # Builds three pics
        page.setLayout(self.upper_box)
        return page

    def set_icon_modes(self, competitor):  # sets up icons and their "filters" [Icon Modes tut]
        icon = QIcon(competitor)  # picture set for icon, defined when called

        pixmap1 = icon.pixmap(400, 400, QIcon.Active, QIcon.On)  # creates pixmap object of modified icon pic
        label1 = QLabel(self)  # label created
        label1.setPixmap(pixmap1)  # label set to display icon's pixmap
        label1.setToolTip("Pure")  # Hover over image msg [Tooltip tut]
        self.upper_box.addWidget(label1)

        pixmap2 = icon.pixmap(400, 400, QIcon.Disabled, QIcon.Off)
        label2 = QLabel(self)
        label2.setPixmap(pixmap2)
        label2.setToolTip("Shaded")
        self.upper_box.addWidget(label2)

        pixmap3 = icon.pixmap(400, 400, QIcon.Selected, QIcon.On)
        label3 = QLabel(self)
        label3.setPixmap(pixmap3)
        label3.setToolTip("Tinted")
        self.upper_box.addWidget(label3)

    def set_about(self):  # Two Methods to create about button and an about QMessageBox (1 option) when clicked
        # [AboutBox tut]
        btn = QPushButton("About", self)
        self.lower_box.addWidget(btn, 1)
        btn.clicked.connect(self.about_clicked)

    def about_clicked(self):
        QMessageBox.about(self, f"About the {self.category_combo.currentText()} Mr. Olympia",
                          f"A world renowned bodybuilding competition among competitors in the "
                          f"{self.category_combo.currentText()} category.")

    def set_category(self):  # Two Methods to create combo box to select between two categories
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Classic", "Open"])
        self.category_combo.activated.connect(self.switch_category)
        self.lower_box.addWidget(self.category_combo, 1)

    def switch_category(self):
        self.category_stack.setCurrentIndex(self.category_combo.currentIndex())  # Stack follows combo
        self.setWindowTitle(f"{self.category_combo.currentText()} Mr. Olympia")

        self.classic_stack.setCurrentIndex(0)  # Reset
        self.open_stack.setCurrentIndex(0)  # Stacks
        if self.category_combo.currentIndex() == 0:  # Change names in competitor combo box
            self.comp_combo.clear()
            self.comp_combo.addItems(self.classic_names)
        else:
            self.comp_combo.clear()
            self.comp_combo.addItems(self.open_names)

    def set_competitors(self):  # Two methods to create combo box to select between two competitors
        self.comp_combo = QComboBox()
        self.comp_combo.addItems(self.classic_names)
        self.comp_combo.activated.connect(self.switch_competitor)
        self.lower_box.addStretch(7)
        self.lower_box.addWidget(self.comp_combo, 1)

    def switch_competitor(self):
        if self.category_combo.currentIndex() == 0:  # Change names in competitor combo box
            self.classic_stack.setCurrentIndex(self.comp_combo.currentIndex())
        else:
            self.open_stack.setCurrentIndex(self.comp_combo.currentIndex())

    def set_judge(self):  # Two Methods to create judge button and a question QMessageBox (2 options) when clicked
        # [QPushButton tut]
        btn = QPushButton("Judge", self)
        self.lower_box.addWidget(btn, 1)
        btn.clicked.connect(self.judge_clicked)

    def judge_clicked(self):
        # Displays radio button judging window
        self.judge = JudgeRadio()
        self.judge.category = self.category_combo.currentIndex()
        self.judge.set_buttons()
        self.judge.show()


class JudgeRadio(ParentWidget):
    def __init__(self,):
        super().__init__()
        self.category = 0  # Initialized as Classic Judging
        self.init_ui("Who Takes the Crown?", 300, 100)

    def init_ui(self, title, width, height):
        super().init_ui(title, width, height)
        layout = QVBoxLayout()  # Outer Layout
        self.setLayout(layout)
        buttons = QVBoxLayout()  # Vertical layout of buttons
        self.btn1 = QRadioButton()
        self.btn2 = QRadioButton()
        buttons.addWidget(self.btn1)
        buttons.addWidget(self.btn2)

        sub_layout = QHBoxLayout()  # HLayout to space buttons from edge of window
        sub_layout.addStretch(1)
        sub_layout.addLayout(buttons)
        sub_layout.addStretch(5)
        layout.addLayout(sub_layout)

        submit_btn = QPushButton("Submit")  # Submit button appended to outer layout
        submit_btn.clicked.connect(self.submission)
        layout.addWidget(submit_btn)
        layout.setAlignment(submit_btn, Qt.AlignRight)

    def set_buttons(self):
        if self.category == 0:
            self.btn1.setText("Bumstead")
            self.btn2.setText("Ruffin")
        else:
            self.btn1.setText("Elssbiay")
            self.btn2.setText("Curry")

    def opened(self, index):
        # Displays radio button judging window
        self.category = index
        self.set_buttons()
        self.show()

    def submission(self):
        if self.btn2.isChecked():
            myapp.quit()
        elif self.btn1.isChecked():
            self.close()
            self.bar = ProgressBar()
            self.bar.show()
            timer = QTimer(self)
            timer.timeout.connect(self.bar.update_progress)
            timer.start(15)


class ProgressBar(QMainWindow, ParentWidget):  # Creates class ProgressBar inheriting QMainWindow
    # [Progress Bar tut] QStatusBar omitted
    def __init__(self):
        super().__init__()
        self.my_status = QStatusBar()  # Empty status bar to fill QMainWindow
        self.progress_bar = QProgressBar()  # Progress Bar to place in Status Bar
        self.init_ui("Judge IQ", 400, 30)

    def init_ui(self, title, width, height):
        super().init_ui(title, width, height)
        self.move(self.x(), self.y() + 220)  # moves Clock towards bottom of screen (+ > down)
        self.my_status.addWidget(self.progress_bar, 1)  # Adds Progress bar to status bar, 1: stretches to fit window
        self.setStatusBar(self.my_status)  # sets status bar into window

    def update_progress(self):  # Runs progress bar from +1% each time called
        i = self.progress_bar.value()
        if i <= 100:
            i += 1
            self.progress_bar.setValue(i)
        else:
            self.timer.stop()


if __name__ == '__main__':
    myapp = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(myapp.exec_())
