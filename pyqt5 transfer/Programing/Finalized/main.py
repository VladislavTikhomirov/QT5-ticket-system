from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QStatusBar, QToolButton, QStackedLayout, QWidget, QFormLayout, QSpinBox, QLineEdit, QGroupBox, QFrame, QHBoxLayout, QVBoxLayout, QLabel, QRadioButton, QButtonGroup, QGridLayout,QPushButton
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5 import QtCore
import sys
#from Seatmap import seatmap

# Constant for ticket prices 
ticket_price_adult = 10
ticket_price_child = 5
ticket_price_elderly = 5
ticket_price_special = 0
# Cimema hall size 
cinema_rows = 10
cinema_seats_per_row = 20
# Program window size as % from screen
main_window_height = 0.8 
main_window_width = 0.8
# Toolbar size as % from program window
toolbar_height = 0.1
# Strings
main_window_title = "Collyers Theater Resevartion System"
toolbar_button_names = ["Book Tickets", "Payment", "Manage Seats",  "Veiw Revenue", "Search Customer"]

class ToolBar(QToolBar):
    def __init__(self, parent, width, height):
        super(ToolBar, self).__init__(parent)
        self.setMovable(False)
        self.setFixedHeight(int(height*toolbar_height))
        # Calculate the button width, height, subtract place for separators 
        button_names_num = len(toolbar_button_names)
        buttons_width = int( (width - (button_names_num -1) * 12) / button_names_num )
        buttons_height = int(height*toolbar_height)
        # Create Buttons 
        for name in toolbar_button_names:
            button = QToolButton()
            button.setText(name)
            self.addWidget(button)
            # Add Separators between buttons, but not before first and after last buttoms
            if name != toolbar_button_names[button_names_num -1]:
                self.addSeparator()
            button.setFixedWidth(buttons_width)
            button.setFixedHeight(buttons_height)
            button.clicked.connect(self.handle_toolbar_button_click)
            button.setStatusTip(name)
    
    def handle_toolbar_button_click(self, button):
        # Porcess ToolBar click
        button_text = self.sender().text()
        index =  toolbar_button_names.index(button_text)
        # Canhes active layout and call layout init function
        self.parent().layout.setCurrentIndex(index)
        self.parent().UIs[index].setupUI()

class BookTickets(QWidget):
    def __init__(self, width, height):
        super(BookTickets, self).__init__()
        
        mainLayout = QHBoxLayout()

        frameLeft = QFrame(self)

        formLeftLayout = QFormLayout(self)
        formLeftLayout.setVerticalSpacing(50)
        formLeftLayout.setHorizontalSpacing(50)
        formLeftLayout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        self.my_title = QLabel("Select Tickets")
        formLeftLayout.addWidget(self.my_title)

        # Create and add group of radio buttons
        self.my_show1 = QRadioButton('Show 1')
        self.my_show2 = QRadioButton('Show 2')
        self.my_show3 = QRadioButton('Show 3')
        
        self.my_show_group = QButtonGroup()
        self.my_show_group.addButton(self.my_show1)
        self.my_show_group.addButton(self.my_show2)
        self.my_show_group.addButton(self.my_show3)
        
        groupBox = QGroupBox()
        groupBox.setLayout(QVBoxLayout())
        groupBox.layout().addWidget(self.my_show1)
        groupBox.layout().addWidget(self.my_show2)
        groupBox.layout().addWidget(self.my_show3)
        formLeftLayout.addRow("Select a Show", groupBox)
        # Radio button press handler
        self.my_show_group.buttonClicked.connect(self.my_show_clicked)
        
        # Create and add spin boxes
        self.my_adult = QSpinBox()
        formLeftLayout.addRow(f"Adults (£{ticket_price_adult})", self.my_adult)
        self.my_adult.valueChanged.connect(self.setTotal)
        self.my_adult.setFixedWidth(100)
        self.my_adult.setFixedHeight(40)

        self.my_child = QSpinBox()
        formLeftLayout.addRow(f"Children (£{ticket_price_child})", self.my_child)
        self.my_child.valueChanged.connect(self.setTotal)
        self.my_child.setFixedWidth(100)
        self.my_child.setFixedHeight(40)

        self.my_elderly = QSpinBox()
        formLeftLayout.addRow(f"Elderly (£{ticket_price_elderly})", self.my_elderly)
        self.my_elderly.valueChanged.connect(self.setTotal)
        self.my_elderly.setFixedWidth(100)
        self.my_elderly.setFixedHeight(40)

        self.my_special = QSpinBox()
        formLeftLayout.addRow(f"Special (£{ticket_price_special})", self.my_special)
        self.my_special.valueChanged.connect(self.setTotal)
        self.my_special.setFixedWidth(100)
        self.my_special.setFixedHeight(40)

        # Create and add total
        self.my_total = QLabel()
        formLeftLayout.addRow("Total Price:",self.my_total)
        self.my_total.setText("£ 0")
    
        self.my_button = QToolButton()
        self.my_button.setText("Next >>")
        formLeftLayout.addWidget(self.my_button)

        frameLeft.setLayout(formLeftLayout)
        mainLayout.addWidget(frameLeft)
        frameLeft.setFixedWidth(int(width/3)) 

        frameRight = QFrame(self)

        formRightLayout = QFormLayout(self)
        formRightLayout.setVerticalSpacing(50)
        formRightLayout.setHorizontalSpacing(50)
        formRightLayout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        self.my_title = QLabel("Seats map:")
        formRightLayout.addWidget(self.my_title)
        
        SetMapUI = SeatMap()
        formRightLayout.addWidget(SetMapUI)
        
        frameRight.setLayout(formRightLayout)
        mainLayout.addWidget(frameRight)
       
        self.setLayout(mainLayout)

    def setTotal(self):
        total_places = self.my_adult.value() + self.my_child.value() + self.my_elderly.value() + self.my_special.value()

        adult_prise = (self.my_adult.value() * ticket_price_adult)
        child_price = (self.my_child.value() * ticket_price_child)
        elderly_price = (self.my_elderly.value() * ticket_price_elderly)
        special_price = (self.my_special.value() * ticket_price_special)
        total_price = '£' + str (adult_prise + child_price + elderly_price + special_price)
        
        if  total_places > cinema_rows * cinema_seats_per_row:
            sender = self.sender()
            sender_value = sender.value()
            sender.setValue(sender_value -1)
        else:
            self.my_total.setText(str(total_price))
            
    def my_show_clicked(self, button):
        if button.isChecked():
            if button.text() == 'Show 1':
                self.show = 1
            elif button.text() == 'Show 2':
                self.show = 2
            else:
                self.show = 3
            #self.seatmap = seatmap(main_window_width, main_window_height, self.show)
            #self.seatmap.show()
            
        print(self.show)   

    def setupUI(self):
        print("TODO")

class Payment(QWidget):
    def __init__(self):
        super(Payment, self).__init__()
        formLayout = QFormLayout(self)
        self.setLayout(formLayout)

        self.lnNameOfCard = QLineEdit()
        self.lnNameOfCard.setObjectName("lnNameOfCard")
        self.lnNameOfCard.setFixedWidth(250)
        self.lnNameOfCard.setFixedHeight(30)
        formLayout.addRow("Name on Card:", self.lnNameOfCard)

        self.lnCardNumber = QLineEdit()
        self.lnCardNumber.setObjectName("lnCardNumber")
        self.lnCardNumber.setFixedWidth(250)
        self.lnCardNumber.setFixedHeight(30)
        formLayout.addRow("Card Number:", self.lnCardNumber)
    
    def setupUI(self):
        print("TODO")

class ManageSeats(QWidget):
    def __init__(self):
        super(ManageSeats, self).__init__()
        formLayout = QFormLayout(self)
        formLayout.addRow("View Seats:", QSpinBox())
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

class SeatMap(QWidget):
    def __init__(self):
        super(SeatMap, self).__init__()
        mainLayout = QVBoxLayout()

        seatsFrame = QFrame(self)
     
        screenFrame = QFrame()
        screenFrame.setFixedHeight(50)
        screenFrame.setStyleSheet('background-color: black;')
        screenLayout = QVBoxLayout()
        screenLabel = QLabel("Screen")
        screenLabel.setStyleSheet('color: white; font-size: 18px;')
        screenLayout.addWidget(screenLabel)
        screenFrame.setLayout(screenLayout)
        
        seatsLayout = QGridLayout()
        for row in range(0,cinema_rows):
            for seat in range(0,cinema_seats_per_row):
                button = QPushButton(chr(97+row).upper() + str(seat))
                button.setFixedSize(60, 60)
                seatsLayout.addWidget(button, row, seat)

        seatsFrame.setLayout(seatsLayout)

        mainLayout.addWidget(screenFrame)
        mainLayout.addWidget(seatsFrame)
        self.setLayout(mainLayout)
    
    def setupUI(self):
        print("TODO")

class MainWindow(QMainWindow):
    def __init__(self, width, height):
        super(MainWindow, self).__init__()
        self.setWindowTitle(main_window_title)
        self.setFixedSize(QSize(width,height))     
        
        # Add Tool Bar
        toolbar = ToolBar(self,width,height)
        self.addToolBar(toolbar)
        
        # Add Status Bar
        statusbar = QStatusBar(self)
        self.setStatusBar(statusbar)

        # Add widgets
        self.layout = QStackedLayout()
        
        BookTicketsUI = BookTickets(width,height)
        self.layout.addWidget(BookTicketsUI)

        PaymentUI = Payment()
        self.layout.addWidget(PaymentUI)

        ManageSeatsUI = ManageSeats()
        self.layout.addWidget(ManageSeatsUI)

        ViewRevenueUI = ViewRevenue()
        self.layout.addWidget(ViewRevenueUI)
        
        SearchCustomerUI = SearchCustomer()
        self.layout.addWidget(SearchCustomerUI)

        # UI list will hold references for windows
        self.UIs = [BookTicketsUI, ManageSeatsUI, PaymentUI, ViewRevenueUI, SearchCustomerUI]
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

def main():
    app = QApplication(sys.argv)
    # Get the screen resolution
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    width =  int(width * main_window_width)
    height = int(height * main_window_height)
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