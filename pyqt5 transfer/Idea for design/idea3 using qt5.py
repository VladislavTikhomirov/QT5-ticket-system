import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLabel, QLineEdit, QGridLayout, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
 
 
class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'Theatre Ticket System'
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 600
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        # Create menu bar
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        helpMenu = mainMenu.addMenu('Help')
        # Add QAction to menu bar
        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # Create buttons
        bookTicketButton = QPushButton('Book Ticket', self)
        searchCustomerButton = QPushButton('Search Customer', self)
        viewPerformanceRevenueButton = QPushButton('View Performance Revenue', self)
        blockSeatsButton = QPushButton('Block Seats', self)
        saveDataButton = QPushButton('Save Data', self)

        # Create labels
        customerNameLabel = QLabel('Name:', self)
        customerTypeLabel = QLabel('Type:', self)
        customerPhoneNumberLabel = QLabel('Phone Number:', self)
        performanceDateLabel = QLabel('Performance Date:', self)
        seatBookedLabel = QLabel('Seat Booked:', self)
        pricePaidLabel = QLabel('Price Paid:', self)

        # Create textboxes
        customerNameTextbox = QLineEdit(self)
        customerTypeTextbox = QLineEdit(self)
        customerPhoneNumberTextbox = QLineEdit(self)
        performanceDateTextbox = QLineEdit(self)
        seatBookedTextbox = QLineEdit(self)
        pricePaidTextbox = QLineEdit(self)

        # Create grid
        gridLayout = QGridLayout()
        gridLayout.setSpacing(10)
 
        gridLayout.addWidget(bookTicketButton, 0, 0)
        gridLayout.addWidget(searchCustomerButton, 0, 1)
        gridLayout.addWidget(viewPerformanceRevenueButton, 0, 2)
        gridLayout.addWidget(blockSeatsButton, 0, 3)
        gridLayout.addWidget(saveDataButton, 0, 4)
        gridLayout.addWidget(customerNameLabel, 1, 0)
        gridLayout.addWidget(customerTypeLabel, 2, 0)
        gridLayout.addWidget(customerPhoneNumberLabel, 3, 0)
        gridLayout.addWidget(performanceDateLabel, 4, 0)
        gridLayout.addWidget(seatBookedLabel, 5, 0)
        gridLayout.addWidget(pricePaidLabel, 6, 0)
        gridLayout.addWidget(customerNameTextbox, 1, 1)
        gridLayout.addWidget(customerTypeTextbox, 2, 1)
        gridLayout.addWidget(customerPhoneNumberTextbox, 3, 1)
        gridLayout.addWidget(performanceDateTextbox, 4, 1)
        gridLayout.addWidget(seatBookedTextbox, 5, 1)
        gridLayout.addWidget(pricePaidTextbox, 6, 1)
 
        window = QWidget()
        window.setLayout(gridLayout)
        self.setCentralWidget(window)
        self.show()
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
