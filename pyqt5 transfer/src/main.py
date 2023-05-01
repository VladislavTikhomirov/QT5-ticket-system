from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QStatusBar, QToolButton, QStackedLayout, QWidget, QFormLayout, QSpinBox, QLineEdit, QGroupBox, QFrame, QHBoxLayout, QVBoxLayout, QLabel, QRadioButton, QButtonGroup, QGridLayout,QPushButton
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5 import QtCore
import sys
import resources as res

class ToolBar(QToolBar):
    def __init__(self, main_window, width, height):
        super(ToolBar, self).__init__(main_window)
        self.my_main_window = main_window 
        self.setMovable(False)
        self.setFixedHeight(int(height*res.toolbar_height))
        # Calculate the button width, height, subtract place for separators 
        my_button_names_num = len(res.toolbar_button_names)
        my_buttons_width = int( (width - (my_button_names_num -1) * 12) / my_button_names_num )
        my_buttons_height = int(height*res.toolbar_height)
        # Create Buttons 
        for my_name in res.toolbar_button_names:
            my_button = QToolButton()
            my_button.setText(my_name)
            self.addWidget(my_button)
            # Add Separators between buttons, but not before first and after last buttoms
            if my_name != res.toolbar_button_names[my_button_names_num -1]:
                self.addSeparator()
            my_button.setFixedWidth(my_buttons_width)
            my_button.setFixedHeight(my_buttons_height)
            my_button.clicked.connect(self.handle_toolbar_button_click)
            my_button.setStatusTip(my_name)
    
    def handle_toolbar_button_click(self):
        # Porcess ToolBar click
        my_button_text = self.sender().text()
        my_index =  res.toolbar_button_names.index(my_button_text)
        # Changes active layout
        self.my_main_window.layout.setCurrentIndex(my_index)

class BookTickets(QWidget):
    def __init__(self, main_window, width, height):
        super(BookTickets, self).__init__(main_window)
        
        self.my_main_window = main_window 
        my_main_layout = QHBoxLayout()
        # left Panel of UI
        my_frame_left = QFrame(self)
        my_form_left_layout = QVBoxLayout()

        # Add Label
        my_form_left_layout.addWidget(QLabel(res.tickets_left_header), 0)

        # Add group of radio buttons
        my_show1 = QRadioButton('Show 1')
        my_show2 = QRadioButton('Show 2')
        my_show3 = QRadioButton('Show 3')

        my_show1.setChecked(True)
        
        self.my_show_group = QButtonGroup()
        self.my_show_group.addButton(my_show1)
        self.my_show_group.addButton(my_show2)
        self.my_show_group.addButton(my_show3)

        my_group_box = QGroupBox()
        my_group_box.setLayout(QVBoxLayout())
        my_group_box.layout().addWidget(my_show1)
        my_group_box.layout().addWidget(my_show2)
        my_group_box.layout().addWidget(my_show3)

        self.my_show_group.buttonClicked.connect(self.handle_radio_button_clicked)
        my_form_left_layout.addWidget(my_group_box,0)
        
        # Add Space & Label
        my_form_left_layout.addWidget(QLabel(""), 0)
        my_form_left_layout.addWidget(QLabel(res.tickets_left_middle), 0)

        # Add groups of spinners
        my_spinners_layout = QFormLayout()
        self.my_adult = QSpinBox()
        my_spinners_layout.addRow(f"Adults (£{res.ticket_price_adult})", self.my_adult)
        self.my_adult.valueChanged.connect(self.handle_spinners_change)
        self.my_adult.setFixedWidth(100)
        self.my_adult.setFixedHeight(40)

        self.my_child = QSpinBox()
        my_spinners_layout.addRow(f"Children (£{res.ticket_price_child})", self.my_child)
        self.my_child.valueChanged.connect(self.handle_spinners_change)
        self.my_child.setFixedWidth(100)
        self.my_child.setFixedHeight(40)

        self.my_elderly = QSpinBox()
        my_spinners_layout.addRow(f"Elderly (£{res.ticket_price_elderly})", self.my_elderly)
        self.my_elderly.valueChanged.connect(self.handle_spinners_change)
        self.my_elderly.setFixedWidth(100)
        self.my_elderly.setFixedHeight(40)

        self.my_special = QSpinBox()
        my_spinners_layout.addRow(f"Special (£{res.ticket_price_special})", self.my_special)
        self.my_special.valueChanged.connect(self.handle_spinners_change)
        self.my_special.setFixedWidth(100)
        self.my_special.setFixedHeight(40)

        # Add total
        self.my_total = QLabel()
        my_spinners_layout.addRow("Total Price, £",self.my_total)
        self.my_total.setText("0")
    
        my_spinners_widget = QWidget(self)
        my_spinners_widget.setLayout(my_spinners_layout)
        my_spinners_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        my_spinners_layout.setVerticalSpacing(20)
        my_form_left_layout.addWidget(my_spinners_widget,1)

        # Add reset button
        my_button_reset_1 = QPushButton("Reset")
        my_form_left_layout.addWidget(my_button_reset_1)
        my_button_reset_1.clicked.connect(self.handle_reset_button_click_1)

        my_frame_left.setLayout(my_form_left_layout)
        my_main_layout.addWidget(my_frame_left, 0)
        
        # Right Panel of UI
        my_frame_right = QFrame(self)
        my_form_right_layout = QVBoxLayout()
        
        # Add Label
        my_form_right_layout.addWidget(QLabel(res.tickets_right_header), 0)
        
        # Add SeatMap
        self.my_seat_map = SeatMap(self.my_main_window)
        my_form_right_layout.addWidget(self.my_seat_map, 1)

        # Add reset button
        my_button_reset_2 = QPushButton("Reset")
        my_form_right_layout.addWidget(my_button_reset_2)
        my_button_reset_2.clicked.connect(self.handle_reset_button_click_2)
    
        my_frame_right.setLayout(my_form_right_layout)
        my_main_layout.addWidget(my_frame_right,1)
       
        self.setLayout(my_main_layout)

    def handle_spinners_change(self):
        total_places = self.get_total_seats()

        adult_prise = (self.my_adult.value() * res.ticket_price_adult)
        child_price = (self.my_child.value() * res.ticket_price_child)
        elderly_price = (self.my_elderly.value() * res.ticket_price_elderly)
        special_price = (self.my_special.value() * res.ticket_price_special)
        total_price = adult_prise + child_price + elderly_price + special_price
        
        if  total_places > res.cinema_rows * res.cinema_seats_per_row:
            sender = self.sender()
            sender_value = sender.value()
            sender.setValue(sender_value -1)
        else:
            self.my_total.setText(str(total_price))
            self.reset_right_form()
         
    def handle_radio_button_clicked(self, button):
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
        my_total = self.my_adult.value() + self.my_child.value() + self.my_elderly.value() + self.my_special.value()
        return my_total

    def reset_left_form(self):
        my_buttons_list = self.my_show_group.buttons()
        my_buttons_list[0].setChecked(True)
        self.my_adult.setValue(0)
        self.my_child.setValue(0)
        self.my_elderly.setValue(0)
        self.my_special.setValue(0)

    def reset_right_form(self):
        self.my_seat_map.reset_setas(self.get_total_seats())
        
    def handle_reset_button_click_1(self, button):
        self.reset_left_form()
        self.reset_right_form()
    
    def handle_reset_button_click_2(self, button):
        self.reset_right_form()

class Payment(QWidget):
    def __init__(self,main_window):
        super(Payment, self).__init__(main_window)

        self.my_main_window = main_window 
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

        self.my_main_window = main_window 
        formLayout = QFormLayout(self)
        formLayout.addRow("View Seats:", QSpinBox())
        self.setLayout(formLayout)

class ViewRevenue(QWidget):
    def __init__(self,main_window):
        super(ViewRevenue, self).__init__(main_window)

        self.my_main_window = main_window 
        formLayout = QFormLayout(self)
        formLayout.addRow("View Revenue:", QSpinBox())
        self.setLayout(formLayout)

class SearchCustomer(QWidget):
    def __init__(self,main_window):
        super(SearchCustomer, self).__init__(main_window)

        self.my_main_window = main_window 
        formLayout = QFormLayout(self)
        formLayout.addRow("Search Customer:", QSpinBox())
        self.setLayout(formLayout)

class SeatMap(QWidget):
    def __init__(self,main_window):
        super(SeatMap, self).__init__(main_window)

        self.my_main_window = main_window 
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
        
        self.seatsLayout = QGridLayout()
        for row in range(0,res.cinema_rows):
            for seat in range(0,res.cinema_seats_per_row):
                button = QPushButton(chr(97+row).upper() + str(seat))
                button.setFixedSize(30, 30)
                self.seatsLayout.addWidget(button, row, seat)
                button.setCheckable(True)
                button.clicked.connect(self.handle_button_clicked)

        seatsFrame.setLayout(self.seatsLayout)
        mainLayout.addWidget(screenFrame)
        mainLayout.addWidget(seatsFrame)
        self.setLayout(mainLayout)

        self.set_max_selectable_seats(res.cinema_rows * res.cinema_seats_per_row)
        self.selected_seats = []

    def handle_button_clicked(self):
        button = self.sender()
        if button.isChecked():
            if len(self.selected_seats) <= self.get_max_selectable_seats()-1:
                self.selected_seats.append(button.text())
            else:
                button.setChecked(False)
        else:
            self.selected_seats.remove(button.text())

    def reset_setas(self, max):
        my_rows = self.seatsLayout.rowCount()
        my_cols = self.seatsLayout.columnCount()
        for my_row in range(my_rows):
            for my_col in range(my_cols):
                my_button_item  = self.seatsLayout.itemAtPosition(my_row, my_col)
                if my_button_item  is not None:
                    my_button_widget = my_button_item.widget()
                    if isinstance(my_button_widget, QPushButton):
                        my_button_widget.setChecked(False)
        
        self.selected_seats = []
        self.set_max_selectable_seats(max)

    def set_max_selectable_seats(self, max):
        self.max_selectable_seats = max

    def get_max_selectable_seats(self):
        return self.max_selectable_seats

class MainWindow(QMainWindow):
    def __init__(self, width, height):
        super(MainWindow, self).__init__()
        self.setWindowTitle(res.main_window_title)
        self.setFixedSize(QSize(width,height))     
        
        # Add Tool Bar
        my_toolbar = ToolBar(self,width,height)
        self.addToolBar(my_toolbar)
        
        # Add Status Bar
        my_statusbar = QStatusBar(self)
        self.setStatusBar(my_statusbar)

        # Add widgets
        self.layout = QStackedLayout()
        
        my_book_tickets_UI = BookTickets(self,width,height)
        self.layout.addWidget(my_book_tickets_UI)

        my_payment_UI = Payment(self)
        self.layout.addWidget(my_payment_UI)

        my_manage_seats_UI = ManageSeats(self)
        self.layout.addWidget(my_manage_seats_UI)

        my_view_revenue_UI = ViewRevenue(self)
        self.layout.addWidget(my_view_revenue_UI)
        
        my_search_customer_UI = SearchCustomer(self)
        self.layout.addWidget(my_search_customer_UI)

        # UI list will hold references for windows
        self.my_UI = [my_book_tickets_UI, my_manage_seats_UI, my_payment_UI, my_view_revenue_UI, my_search_customer_UI]
        my_widget = QWidget()
        my_widget.setLayout(self.layout)
        self.setCentralWidget(my_widget)

def main():
    my_app = QApplication(sys.argv)
    # Get the screen resolution
    my_screen_resolution = my_app.desktop().screenGeometry()
    my_width, my_height = my_screen_resolution.width(), my_screen_resolution.height()
    my_width =  int(my_width * res.main_window_width)
    my_height = int(my_height * res.main_window_height)
    my_window = MainWindow(my_width,my_height)
    my_window.show()
    # Read the QSS file and apply style sheet globally
    with open("./pyqt5 transfer/src/style.qss", "r") as f:
        _style = f.read()
        my_app.setStyleSheet(_style)
    # Start the event loop.
    my_app.exec()
    #Your application won't reach here until you exit

if __name__ == "__main__":
    main()