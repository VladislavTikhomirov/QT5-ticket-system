#include the necessary libraries
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

#define a class for the main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Main Window'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

#define a function to initialize the UI
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar().showMessage('Ready')

#define a function to open the second window
        self.open_window2()

#define a function to open the third window
        self.open_window3()

#define a function to open the fourth window
        self.open_window4()

#define a function to open the fifth window
        self.open_window5()

#define a function to open the sixth window
        self.open_window6()
        self.show()

#define a function to open the second window
    def open_window2(self):
        self.home = Window2()
        self.home.show()

#define a function to open the third window
    def open_window3(self):
        self.window3 = Window3()
        self.window3.show()

#define a function to open the fourth window
    def open_window4(self):
        self.window4 = Window4()
        self.window4.show()

#define a function to open the fifth window
    def open_window5(self):
        self.window5 = Window5()
        self.window5.show()

#define a function to open the sixth window
    def open_window6(self):
        self.window6 = Window6()
        self.window6.show()

#define a class for the second window
class Window2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Window 2'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
#define a class for the third window
class Window3(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Window 3'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

#define a function to initialize the UI
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar().showMessage('Ready')

#define a class for the fourth window
class Window4(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Window 4'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

#define a function to initialize the UI
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar().showMessage('Ready')

#define a class for the fifth window
class Window5(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Window 5'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

#define a function to initialize the UI
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar().showMessage('Ready')

#define a class for the sixth window
class Window6(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Window 6'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

#define a function to initialize the UI
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar().showMessage('Ready')

#run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
