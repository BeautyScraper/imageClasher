import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction, QShortcut
from PyQt5.QtGui import QKeySequence

def new_file():
    print("New file was clicked")

def open_file():
    print("Open file was clicked")

def save_file():
    print("Save file was clicked")

def exit_application():
    app.quit()

def toggle_menu_bar():
    menubar.setVisible(not menubar.isVisible())

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("PyQt5 Menu Example")
window.setGeometry(100, 100, 800, 600)

menubar = window.menuBar()
menubar.setVisible(False)
file_menu = menubar.addMenu("File")

new_action = QAction("New", window)
file_menu.addAction(new_action)

open_action = QAction("Open", window)
file_menu.addAction(open_action)

save_action = QAction("Save", window)
file_menu.addAction(save_action)

exit_action = QAction("Exit", window)
file_menu.addAction(exit_action)

new_action.triggered.connect(new_file)
open_action.triggered.connect(open_file)
save_action.triggered.connect(save_file)
exit_action.triggered.connect(exit_application)

# Create a shortcut to toggle the menu bar with the F11 key
toggle_menu_bar_shortcut = QShortcut(QKeySequence("F11"), window)
toggle_menu_bar_shortcut.activated.connect(toggle_menu_bar)

window.show()
sys.exit(app.exec_())
