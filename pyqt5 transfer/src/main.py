from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QStatusBar, QToolButton, QStackedLayout, QWidget, QFormLayout, QSpinBox, QLineEdit, QGroupBox, QFrame, QHBoxLayout, QVBoxLayout, QLabel, QRadioButton, QButtonGroup, QGridLayout,QPushButton
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5 import QtCore
import sys
import resources as res

class ToolBar(QToolBar):
    def __init__(self, main_window, width, height):
        super(ToolBar, self).__init__(main_window)
        self.main_window = main_window 
        self.setMovable(False)
        self.setFixedHeight(int(height*res.toolbar_height))
        # Calculate the button width, height, subtract place for separators 
        button_names_num = len(res.toolbar_button_names)
        buttons_width = int( (width - (button_names_num -1) * 12) / button_names_num )
        buttons_height = int(height*res.toolbar_height)
        # Create Buttons 
        for name in res.toolbar_button_names:
            button = QToolButton()
            button.setText(name)
            self.addWidget(button)
            # Add Separators between buttons, but not before first and after last buttoms
            if name != res.toolbar_button_names[button_names_num -1]:
                self.addSeparator()
            button.setFixedWidth(buttons_width)
            button.setFixedHeight(buttons_height)
            button.clicked.connect(self.handle_toolbar_button_click)
            button.setStatusTip(name)
    
    def handle_toolbar_button_click(self, button):
        # Porcess ToolBar click
        button_text = self.sender().text()
        index =  res.toolbar_button_names.index(button_text)
        # Canhes active layout and call layout init function
        self.main_window.layout.setCurrentIndex(index)
        #self.parent().UIs[index].setupUI()

class BookTickets(QWidget):
    def __init__(self, main_window, width, height):
        super(BookTickets, self).__init__(main_window)
        
        self.main_window = main_window 
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
        formLeftLayout.addRow(f"Adults (£{res.ticket_price_adult})", self.my_adult)
        self.my_adult.valueChanged.connect(self.setTotal)
        self.my_adult.setFixedWidth(100)
        self.my_adult.setFixedHeight(40)

        self.my_child = QSpinBox()
        formLeftLayout.addRow(f"Children (£{res.ticket_price_child})", self.my_child)
        self.my_child.valueChanged.connect(self.setTotal)
        self.my_child.setFixedWidth(100)
        self.my_child.setFixedHeight(40)

        self.my_elderly = QSpinBox()
        formLeftLayout.addRow(f"Elderly (£{res.ticket_price_elderly})", self.my_elderly)
        self.my_elderly.valueChanged.connect(self.setTotal)
        self.my_elderly.setFixedWidth(100)
        self.my_elderly.setFixedHeight(40)

        self.my_special = QSpinBox()
        formLeftLayout.addRow(f"Special (£{res.ticket_price_special})", self.my_special)
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
        
        SetMapUI = SeatMap(self.main_window)
        formRightLayout.addWidget(SetMapUI)
        
        frameRight.setLayout(formRightLayout)
        mainLayout.addWidget(frameRight)
       
        self.setLayout(mainLayout)

    def setTotal(self):
        total_places = self.get_total_seats()

        adult_prise = (self.my_adult.value() * res.ticket_price_adult)
        child_price = (self.my_child.value() * res.ticket_price_child)
        elderly_price = (self.my_elderly.value() * res.ticket_price_elderly)
        special_price = (self.my_special.value() * res.ticket_price_special)
        total_price = '£' + str (adult_prise + child_price + elderly_price + special_price)
        
        if  total_places > res.cinema_rows * res.inema_seats_per_row:
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

    def get_total_seats(self):
        total = self.my_adult.value() + self.my_child.value() + self.my_elderly.value() + self.my_special.value()
        return total

class Payment(QWidget):
    def __init__(self,main_window):
        super(Payment, self).__init__(main_window)

        self.main_window = main_window 
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
    
class ManageSeats(QWidget):
    def __init__(self,main_window):
        super(ManageSeats, self).__init__(main_window)

        self.main_window = main_window 
        formLayout = QFormLayout(self)
        formLayout.addRow("View Seats:", QSpinBox())
        self.setLayout(formLayout)

class ViewRevenue(QWidget):
    def __init__(self,main_window):
        super(ViewRevenue, self).__init__(main_window)

        self.main_window = main_window 
        formLayout = QFormLayout(self)
        formLayout.addRow("View Revenue:", QSpinBox())
        self.setLayout(formLayout)

class SearchCustomer(QWidget):
    def __init__(self,main_window):
        super(SearchCustomer, self).__init__(main_window)

        self.main_window = main_window 
        formLayout = QFormLayout(self)
        formLayout.addRow("Search Customer:", QSpinBox())
        self.setLayout(formLayout)

class SeatMap(QWidget):
    def __init__(self,main_window):
        super(SeatMap, self).__init__(main_window)

        self.main_window = main_window 
        mainLayout = QVBoxLayout()

        seatsFrame = QFrame(self)

        screenFrame = QFrame()
        screenFrame.setFixedHeight(40)
        screenFrame.setStyleSheet('background-color: black;')
        screenLayout = QVBoxLayout()
        screenLabel = QLabel("Screen")
        screenLabel.setStyleSheet('color: white; font-size: 10px;')
        screenLayout.addWidget(screenLabel)
        screenFrame.setLayout(screenLayout)
        
        seatsLayout = QGridLayout()
        for row in range(0,res.cinema_rows):
            for seat in range(0,res.cinema_seats_per_row):
                button = QPushButton(chr(97+row).upper() + str(seat))
                button.setFixedSize(30, 30)
                seatsLayout.addWidget(button, row, seat)
                button.setCheckable(True)
                button.clicked.connect(self.button_clicked)

        seatsFrame.setLayout(seatsLayout)

        mainLayout.addWidget(screenFrame)
        mainLayout.addWidget(seatsFrame)
        self.setLayout(mainLayout)

        self.selected_seats = []

    def button_clicked(self):
        button = self.sender()

        index = self.main_window.layout.currentIndex()
        #check = self.main_window.UIs[0].get_to
        if button.isChecked():
            self.selected_seats.append(button.text())
        else:
            self.selected_seats.sort()
            self.selected_seats.remove(button.text())
        print('Selected seats:', self.selected_seats)

class MainWindow(QMainWindow):
    def __init__(self, width, height):
        super(MainWindow, self).__init__()
        self.setWindowTitle(res.main_window_title)
        self.setFixedSize(QSize(width,height))     
        
        # Add Tool Bar
        toolbar = ToolBar(self,width,height)
        self.addToolBar(toolbar)
        
        # Add Status Bar
        statusbar = QStatusBar(self)
        self.setStatusBar(statusbar)

        # Add widgets
        self.layout = QStackedLayout()
        
        BookTicketsUI = BookTickets(self,width,height)
        self.layout.addWidget(BookTicketsUI)

        PaymentUI = Payment(self)
        self.layout.addWidget(PaymentUI)

        ManageSeatsUI = ManageSeats(self)
        self.layout.addWidget(ManageSeatsUI)

        ViewRevenueUI = ViewRevenue(self)
        self.layout.addWidget(ViewRevenueUI)
        
        SearchCustomerUI = SearchCustomer(self)
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
    width =  int(width * res.main_window_width)
    height = int(height * res.main_window_height)
    window = MainWindow(width,height)
    window.show()
    # Read the QSS file and apply style sheet globally
    with open("./pyqt5 transfer/src/style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    # Start the event loop.
    app.exec()
    #Your application won't reach here until you exit

if __name__ == "__main__":
    main()