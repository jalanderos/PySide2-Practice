import sys
from PySide2.QtWidgets import QApplication, QTextEdit, QWidget, QPushButton, QMainWindow, \
    QDockWidget, QFormLayout, QFileDialog, QLineEdit, QCheckBox
from PySide2.QtGui import QIcon, QTextCursor, QTextDocument, QPixmap
from PySide2.QtCore import Qt, Signal, Slot
import os
print(os.getcwd())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.text_edit = QTextEdit()
        # self.text_edit.setStyleSheet("background-color: orange; "
        #                             "font-size: 16pt; font-weight: bold;")
        self.setCentralWidget(self.text_edit)

        self.menu = self.menuBar()  # Create a QMenuBar
        self.set_file_menu()
        self.set_edit_toolbar()
        self.set_find_dock()
        self.statusBar().showMessage("Welcome to my editor", 3000)  # QStatusBar created with msg

    def set_file_menu(self):  # Create a file QMenu and add QAction's
        file_menu = self.menu.addMenu("File")  # QMenu
        file_menu.addAction("Open", self.open_file)  # QAction
        file_menu.addAction("Save", self.save_file)  # QAction
        file_menu.addSeparator()
        file_menu.addAction("Quit", self.close)  # QAction

    def open_file(self):  # Called on clicking Open in File Menu
        filename, _ = QFileDialog.getOpenFileName()
        if filename:  # if file is returned
            with open(filename, 'r') as handle:
                text = handle.read()  # Take text from txt file
            self.text_edit.clear()
            self.text_edit.insertPlainText(text)
            self.text_edit.moveCursor(QTextCursor.Start)
            self.statusBar().showMessage(f'Editing {filename}')  # QStatusBar created with msg

    def save_file(self):  # Called on clicking Save in File Menu
        text = self.text_edit.toPlainText()  # Take text from text edit
        filename, _ = QFileDialog.getSaveFileName()  # Prompt for file name
        if filename:
            with open(filename, 'w') as handle:
                handle.write(text)
            self.statusBar().showMessage(f'Saved to {filename}', 5000)

    def set_edit_toolbar(self):  # Create an edit QToolBar
        edit_toolbar = self.addToolBar("Edit")
        edit_toolbar.addAction(QIcon(QPixmap("Icons/copy.svg")), "Copy", self.text_edit.copy)
        edit_toolbar.addAction(QIcon(QPixmap("Icons/cut.svg")), "Cut", self.text_edit.cut)
        edit_toolbar.addAction(QIcon(QPixmap("Icons/paste.svg")), "Paste", self.text_edit.paste)
        edit_toolbar.addAction(QIcon(QPixmap("Icons/undo.svg")), "Undo", self.text_edit.undo)
        edit_toolbar.addAction(QIcon(QPixmap("Icons/redo.svg")), "Redo", self.text_edit.redo)

    def set_find_dock(self):  # Create a QDockWidget to find text in text edit
        find_dock = QDockWidget("Find")
        find_widget = FindWidget()
        find_dock.setWidget(find_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, find_dock)
        find_widget.submitted.connect(self.find)

    @Slot(str, bool)
    def find(self, term, case_sensitive=False):  # find term in text either case sensitive or not
        # Searching both forwards and backwards
        back = QTextDocument.FindBackward  # Create flag for backwards search
        if case_sensitive:
            cs = QTextDocument.FindCaseSensitively
            back |= cs  # Case Sensitive search appended to backwards search
            found = self.text_edit.find(term, cs) | self.text_edit.find(term, back)
        else:
            found = self.text_edit.find(term) | self.text_edit.find(term, back)
        if not found:
            self.statusBar().showMessage("No Matches Found", 1000)


class FindWidget(QWidget):
    submitted = Signal(str, bool)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.find_input = QLineEdit()
        self.case_checkbox = QCheckBox("Case Sensitive")
        # QIcon is collection of QPixmap's tied to widget state
        find_img = QPixmap("Icons/search.svg")  # Create QPixmap first
        self.submit_btn = QPushButton("Find", icon=QIcon(find_img), clicked=self.submit, objectName="sub_btn")
        self.submit_btn.setEnabled(False)

        self.find_input.textChanged.connect(self.check_term)

        self.setLayout(QFormLayout())
        self.layout().addRow("Find:", self.find_input)
        self.layout().addRow(" ", self.case_checkbox)
        self.layout().addRow(" ", self.submit_btn)

    def check_term(self, term):  # If find_input is not empty, submit_btn is enabled
        if term:
            self.submit_btn.setEnabled(True)
        else:
            self.submit_btn.setEnabled(False)

    def submit(self):
        term = self.find_input.text()
        case_sensitive = (self.case_checkbox.checkState() == Qt.Checked)
        self.submitted.emit(term, case_sensitive)


# Can set background colors, images, margins, padding, borders, font settings
# background-image: url("Photos/CBum.png")
# .QWidget { } would target only QWidget, QWidget { } would target it and all child classes
stylesheet = """
QTextEdit {
    font-size: 14pt; font-weight: bold;
}
QToolBar{
    background-color: lightgrey;
}
#sub_btn {
    border: 1px solid grey; background-color: lightgrey;
}
QCheckBox::indicator:unchecked {
    background-color: lightblue;
}
QCheckBox::indicator:checked {
    background-color: blue;
}
"""

if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myapp.setStyleSheet(stylesheet)
    mw = MainWindow()
    sys.exit(myapp.exec_())
