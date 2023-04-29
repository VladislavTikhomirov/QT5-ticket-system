from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDoubleSpinBox, QToolBar, QStatusBar, QToolButton, QStackedLayout, QWidget, QFormLayout
from PyQt5.QtGui import QPalette, QColor
import sys

class ToolBar(QToolBar):
    def __init__(self, parent, width, height):
        super(ToolBar, self).__init__(parent)
        # Toolbar button names
        self.button_names = ["Book Seats", "View Seats", "Payment", "Veiw Revenue", "Search Customer"]
        # Calculate the button width, height
        # 4 pixels per separator, no separators before first and after last buttoms
        # 4 pixels per button for padding
        button_names_num = len(self.button_names)
        separators_width  = (button_names_num -1) * 4 
        padding_width = button_names_num  * 4
        buttons_width = int( (width - separators_width - padding_width) / button_names_num)
        buttons_height = int(height*0.1)
        
        # Create Buttons 
        for name in self.button_names:
            button = QToolButton()
            button.setText(name)
            self.addWidget(button)
            # Add Separators between buttons, but not before first and after last buttoms
            if name != self.button_names[button_names_num -1]:
                self.addSeparator()
            button.setFixedWidth(buttons_width)
            button.setFixedHeight(buttons_height)
            button.clicked.connect(self.handle_toolbar_button_click)
            button.setStatusTip(name)
        self.setMovable(False)
        self.setFixedHeight(int(height*0.1))
    
    def handle_toolbar_button_click(self, button):
        # Route click to the main window handler function
        button_text = self.sender().text()
        index =  self.button_names.index(button_text)
        self.parent().handle_toolbar_button_click(index)

class BookSeats(QWidget):
    def __init__(self):
        super(BookSeats, self).__init__()
        formLayout = QFormLayout(self)
        formLayout.addRow("Book Seats:", QDoubleSpinBox())
        self.setLayout(formLayout)
        self.
    


class ViewSeats(QWidget):
    def __init__(self):
        super(ViewSeats, self).__init__()
        formLayout = QFormLayout(self)
        formLayout.addRow("View Seats:", QDoubleSpinBox())
        self.setLayout(formLayout)

class Payment(QWidget):
    def __init__(self):
        super(Payment, self).__init__()
        formLayout = QFormLayout(self)
        formLayout.addRow("Payment:", QDoubleSpinBox())
        self.setLayout(formLayout)

class ViewRevenue(QWidget):
    def __init__(self):
        super(ViewRevenue, self).__init__()
        formLayout = QFormLayout(self)
        formLayout.addRow("View Revenue:", QDoubleSpinBox())
        self.setLayout(formLayout)

class SearchCustomer(QWidget):
    def __init__(self):
        super(SearchCustomer, self).__init__()
        formLayout = QFormLayout(self)
        formLayout.addRow("Search Customer:", QDoubleSpinBox())
        self.setLayout(formLayout)

class MainWindow(QMainWindow):
    def __init__(self, width, height):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Collyers Theater Resevartion System")
        self.setFixedSize(QSize(width,height))     
        
        #Add Tool Bar
        toolbar = ToolBar("myToolBar",width,height)
        self.addToolBar(toolbar)
        
        #Add Status Bar
        statusbar = QStatusBar(self)
        self.setStatusBar(statusbar)

        self.layout = QStackedLayout()
        self.layout.addWidget(BookSeats())
        self.layout.addWidget(ViewSeats())
        self.layout.addWidget(Payment())
        self.layout.addWidget(ViewRevenue())
        self.layout.addWidget(SearchCustomer())

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
    
    def handle_toolbar_button_click(self, index):
         self.layout.setCurrentIndex(index)

def main():
    app = QApplication(sys.argv)
    # Get the screen resolution
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    width =  int(width * 0.8)
    height = int(height * 0.8)

    window = MainWindow(width,height)
    window.show()
    # Read the QSS file and apply style sheet globally
    with open("./Programing/Finalized/style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    # Start the event loop.
    app.exec()
    #Your application won't reach here until you exit

if __name__ == "__main__":
    main()