from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QStatusBar, QToolButton, QStackedLayout, QWidget, QFormLayout, QSpinBox, QLineEdit, QFrame, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtGui import QPalette, QColor
from PyQt5 import QtCore
import sys

# Constant for ticket prices 
ticket_price_adult = 10
ticket_price_child = 5
ticket_price_elderly = 5
ticket_price_special = 0


class ToolBar(QToolBar):
    def __init__(self, parent, width, height):
        super(ToolBar, self).__init__(parent)
        # Toolbar button names
        self.button_names = ["Book Seats", "View Seats", "Payment", "Veiw Revenue", "Search Customer"]
        # Calculate the button width, height, subtract place for separators 
        button_names_num = len(self.button_names)
        buttons_width = int( (width - (button_names_num -1) * 12) / button_names_num )
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
        # Porcess ToolBar click
        button_text = self.sender().text()
        index =  self.button_names.index(button_text)
        # Canhes active layout and call layout init function
        self.parent().layout.setCurrentIndex(index)
        self.parent().UIs[index].setupUI()

class BookSeats(QWidget):
    def __init__(self, width, height):
        super(BookSeats, self).__init__()

        vbox = QVBoxLayout()

        self.my_title = QLabel()
        self.my_title.setText("Please select number of seats:")
        vbox.addWidget(self.my_title)

        frame = QFrame(self)
        formLayout = QFormLayout(self)
        # control for spinners
        self.my_adult = QSpinBox()
        formLayout.addRow("Adults (£"+str(ticket_price_adult)+"):", self.my_adult)
        
        self.my_child = QSpinBox()
        formLayout.addRow("Children (£"+str(ticket_price_child)+"):", self.my_child)

        self.my_elderly = QSpinBox()
        formLayout.addRow("Elderly (£"+str(ticket_price_elderly)+"):", self.my_elderly)

        self.my_special = QSpinBox()
        formLayout.addRow("Special (£"+str(ticket_price_special)+"):", self.my_special)

        self.my_total = QLineEdit()
        formLayout.addRow("Total Price:",self.my_total)
        self.my_total.setText("£")
        self.my_total.setReadOnly(True)
        
        #Setting boundaries
        formLayout.setVerticalSpacing(40)
        formLayout.setHorizontalSpacing(20)
        frame.setLayout(formLayout)
        vbox.addWidget(frame)
        vbox.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(vbox)
        
        self.setFixedHeight(int(height*0.9))
        self.setFixedWidth(int(width))
        

    def setupUI(self):
        self.my_adult.setValue(5)

class ViewSeats(QWidget):
    def __init__(self):
        super(ViewSeats, self).__init__()
        formLayout = QFormLayout(self)
        formLayout.addRow("View Seats:", QSpinBox())
        self.setLayout(formLayout)
    
    def setupUI(self):
        print("TODO")

class Payment(QWidget):
    def __init__(self):
        super(Payment, self).__init__()
        formLayout = QFormLayout(self)
        formLayout.addRow("Payment:", QSpinBox())
        self.setLayout(formLayout)
    
    def setupUI(self):
        print("TODO")

class ViewRevenue(QWidget):
    def __init__(self):
        super(ViewRevenue, self).__init__()
        formLayout = QFormLayout(self)
        formLayout.addRow("View Revenue:", QSpinBox())
        self.setLayout(formLayout)
    
    def setupUI(self):
        print("TODO")

class SearchCustomer(QWidget):
    def __init__(self):
        super(SearchCustomer, self).__init__()
        formLayout = QFormLayout(self)
        formLayout.addRow("Search Customer:", QSpinBox())
        self.setLayout(formLayout)
    
    def setupUI(self):
        print("TODO")

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

        # Add widgets
        self.layout = QStackedLayout()
        
        BookSeatsUI = BookSeats(width,height)
        self.layout.addWidget(BookSeatsUI)

        ViewSeatsUI = ViewSeats()
        self.layout.addWidget(ViewSeatsUI)

        PaymentUI = Payment()
        self.layout.addWidget(PaymentUI)

        ViewRevenueUI = ViewRevenue()
        self.layout.addWidget(ViewRevenueUI)
        
        SearchCustomerUI = SearchCustomer()
        self.layout.addWidget(SearchCustomerUI)

        self.UIs = [BookSeatsUI, ViewSeatsUI, PaymentUI, ViewRevenueUI, SearchCustomerUI]
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

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
    with open("./pyqt5 transfer/Programing/Finalized/style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    # Start the event loop.
    app.exec()
    #Your application won't reach here until you exit

if __name__ == "__main__":
    main()