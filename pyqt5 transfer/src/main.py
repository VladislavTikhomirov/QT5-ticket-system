from PyQt5.QtCore import QSize, Qt, QRegExp
from PyQt5.QtWidgets import QApplication, QMainWindow,QTableWidget,QComboBox,QTableWidgetItem, QToolBar, QStatusBar, QToolButton, QStackedLayout, QWidget, QFormLayout, QSpinBox, QLineEdit, QGroupBox, QFrame, QHBoxLayout, QVBoxLayout, QLabel, QRadioButton, QButtonGroup, QGridLayout,QPushButton
from PyQt5.QtGui import QKeyEvent, QRegExpValidator
import sys, pyodbc, string
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
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
        self.show = 1
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
        #my_button_reset_1 = QPushButton("Reset")
        #my_form_left_layout.addWidget(my_button_reset_1)
        #my_button_reset_1.clicked.connect(self.handle_reset_button_click_1)

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

        my_button_send_sql_of_right_side = QPushButton("Confirm Seats")
        my_form_right_layout.addWidget(my_button_send_sql_of_right_side)
        my_button_send_sql_of_right_side.clicked.connect(self.handle_send_sql)
        my_button_send_sql_of_right_side.clicked.connect(self.handle_seat_Sql)
        self.my_seat_map.handle_load_sql(1)
        self.my_show_group.buttonClicked.connect(self.handle_radio_button_clicked)
        # Add reset button
        #my_button_reset_2 = QPushButton("Reset")
        #my_form_right_layout.addWidget(my_button_reset_2)
        #my_button_reset_2.clicked.connect(self.handle_reset_button_click_2)

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
        self.my_seat_map.handle_load_sql(self.show)
            #self.seatmap = seatmap(main_window_width, main_window_height, self.show)
            #self.seatmap.show()
            
        print(self.show)
    
    def handle_send_sql(self):
        
        try:
            cs = pyodbc.connect(
                "Driver={SQL Server};"
                "Server=COMPOOTER;"
                "Database=Transfer;"
                "Trusted_Connection=yes;"
            )

            print("Places Connected")

            cursor = cs.cursor()

            # Retrieve the current PaymentID value from the PaymentCounter table
            cursor.execute("SELECT PaymentID FROM PaymentCounter")
            payment_id = cursor.fetchone()[0]

            adult = self.my_adult.value()
            child = self.my_child.value()
            elderly = self.my_elderly.value()
            special = self.my_special.value()
            my_total = adult + child + elderly + special

            if my_total == 0:
                cursor.close()
                cs.close()
            if self.show == 1:
                show = 1
            elif self.show == 2:
                show = 2
            else:
                show = 3

            query = "INSERT INTO Show (ShowID, PaymentID, Adult, Child, Elderly, Special) VALUES (?, ?, ?, ?, ?, ?)"

            my_values = (show, payment_id, adult, child, elderly, special)
            cursor.execute(query, my_values)

            cs.commit()

            cursor.close()
            cs.close()
        except pyodbc.Error as e:
            print(e)

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
        self.my_seat_map.reset_seats(self.get_total_seats())
        
    def handle_reset_button_click_1(self, button):
        self.reset_left_form()
        self.reset_right_form()
    
    def handle_reset_button_click_2(self, button):
        self.reset_right_form()

    def handle_seat_Sql(self):
        self.my_seat_map.handle_confirm_seats_sql(self.show)

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
            for seat in range(1,res.cinema_seats_per_row+1):
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
        self.original_selected_seats = self.selected_seats.copy()

    def handle_button_clicked(self):
        button = self.sender()
        if button.isChecked():
            if len(self.selected_seats) < self.get_max_selectable_seats():
                self.selected_seats.append(button.text())
            else:
                button.setChecked(False)
        else:
            if button.text() not in self.original_selected_seats:
                self.selected_seats.remove(button.text())
            else:
                button.setChecked(True)
    def reset_seats(self, max):
        my_rows = self.seatsLayout.rowCount()
        my_cols = self.seatsLayout.columnCount()
        for my_row in range(my_rows):
            for my_col in range(my_cols):
                my_button_item  = self.seatsLayout.itemAtPosition(my_row, my_col)
                if my_button_item  is not None:
                    my_button_widget = my_button_item.widget()
                    if isinstance(my_button_widget, QPushButton):
                        seat_name = my_button_widget.text()
                        if seat_name in self.selected_seats and seat_name not in self.original_selected_seats:
                            my_button_widget.setChecked(False)
        self.selected_seats = [seat for seat in self.selected_seats if seat in self.original_selected_seats]
        self.set_max_selectable_seats(max)

    def handle_load_sql(self, show):
        try:
            cs = pyodbc.connect(
                "Driver={SQL Server};"
                "Server=COMPOOTER;"
                "Database=Transfer;"
                "Trusted_Connection=yes;"
            )

            print("Seat Loading")
            cursor = cs.cursor()
            cursor.execute("SELECT SeatID FROM Seats WHERE Show = ?", (show,))
            query_seats = cursor.fetchall()

            # Make a list of seat IDs that are already selected for this show
            selected_seats_for_show = []
            for seat in query_seats:
                selected_seats_for_show.append(seat[0])

            # Update the seatmap to reflect the selected seats for this show
            my_rows = self.seatsLayout.rowCount()
            my_cols = self.seatsLayout.columnCount()
            for my_row in range(my_rows):
                for my_col in range(my_cols):
                    my_button_item = self.seatsLayout.itemAtPosition(my_row, my_col)
                    if my_button_item is not None:
                        my_button_widget = my_button_item.widget()
                        if isinstance(my_button_widget, QPushButton):
                            button_text = my_button_widget.text()
                            if button_text in selected_seats_for_show:
                                my_button_widget.setChecked(True)
                                my_button_widget.setEnabled(False)
                            else:
                                my_button_widget.setChecked(False)
                                my_button_widget.setEnabled(True)



            cs.commit()
            cursor.close()
            cs.close()
        except pyodbc.Error as e:
            print(e)


    def set_max_selectable_seats(self, max):
        self.max_selectable_seats = max

    def get_max_selectable_seats(self):
        return self.max_selectable_seats

    def handle_confirm_seats_sql(self, showID):
        try:
            cs = pyodbc.connect(
                "Driver={SQL Server};"
                "Server=COMPOOTER;"
                "Database=Transfer;"
                "Trusted_Connection=yes;"
            )

            print("Seat Appended")

            cursor = cs.cursor()
            cursor.execute("SELECT PaymentID FROM PaymentCounter")
            payment_id = cursor.fetchone()[0]
            seat_status = "Booked"
            for seat in self.selected_seats:
                query = "INSERT INTO Seats (PaymentID, SeatStatus, SeatID, Show) VALUES (?,?,?,?)"
                my_values = (payment_id, seat_status, seat, showID)
                cursor.execute(query, my_values)

            cs.commit()
            cursor.close()
            cs.close()
        except pyodbc.Error as e:
            print(e)

class Payment(QWidget): 
    def __init__(self,main_window):
        super(Payment, self).__init__(main_window)
        self.my_main_window = main_window
        # Create a widget to hold the form
        form_widget = QWidget(self)

        # Set the layout of the widget to a QVBoxLayout
        vbox_layout = QVBoxLayout(form_widget)
        vbox_layout.setAlignment(Qt.AlignCenter)
        form_widget.setLayout(vbox_layout)


        # Add the elements to the QGridLayout
        self.my_card_name = QLineEdit()
        self.my_card_number = QLineEdit()
        self.my_card_expiry = QLineEdit()
        self.my_card_cvv = QLineEdit()
        self.my_confirm_payment = QPushButton("Confirm")
        

        vbox_layout.addWidget(QLabel("Name on Card:"))
        vbox_layout.addWidget(self.my_card_name)
        self.my_card_name.setFixedWidth(500)
        self.my_card_name.setFixedHeight(30)
        # Only accepts letters and 1 space
        validator = QRegExpValidator(self)
        validator.setRegExp(QRegExp(r'^[a-zA-Z]+(\s[a-zA-Z]+)?$'))
        self.my_card_name.setValidator(validator)
        self.my_card_name.setPlaceholderText("A Birling")
        self.my_card_name.textChanged.connect(self.validate_card_name)
        self.my_card_name.setObjectName("my_card_name")

        vbox_layout.addWidget(QLabel("Card Number:"))
        vbox_layout.addWidget(self.my_card_number)
        self.my_card_number.setFixedWidth(500)
        self.my_card_number.setFixedHeight(30)
        self.my_card_number.setMaxLength(16)
        self.my_card_number.setPlaceholderText("XXXXXXXXXXXXXXXX")
        self.my_card_number.textChanged.connect(self.validate_card_number)
        self.my_card_number.setObjectName("my_card_number")

        vbox_layout.addWidget(QLabel("Card Expiry:"))
        vbox_layout.addWidget(self.my_card_expiry)
        self.my_card_expiry.setFixedWidth(70)
        self.my_card_expiry.setFixedHeight(30)
        self.my_card_expiry.setMaxLength(5)
        self.my_card_expiry.setPlaceholderText("MM/YY")
        self.my_card_expiry.textChanged.connect(self.validate_expiry)
        self.my_card_expiry.installEventFilter(self)
        self.my_card_expiry.setObjectName("my_card_expiry")
        

        vbox_layout.addWidget(QLabel("CVV:"))
        vbox_layout.addWidget(self.my_card_cvv)
        self.my_card_cvv.setFixedWidth(50)
        self.my_card_cvv.setFixedHeight(30)
        self.my_card_cvv.setMaxLength(3)
        self.my_card_cvv.setPlaceholderText("123")
        self.my_card_cvv.textChanged.connect(self.validate_cvv)
        self.my_card_cvv.setObjectName("my_card_cvv")

        self.setStyleSheet("QLineEdit{background-color: rgba(255, 0, 0, 0.2);}")

        vbox_layout.addWidget(self.my_confirm_payment)
        self.my_confirm_payment.setFixedHeight(50)
        self.my_confirm_payment.setFixedWidth(70)
        self.my_confirm_payment.clicked.connect(self.handle_payment_sql)
        self.setLayout(vbox_layout)

    # All validation
    def validate_card_name(self, text):
        self.my_card_name.setText(text.upper())
        if len(text) > 0:
            self.my_card_name.setStyleSheet("QLineEdit#my_card_name{background-color: rgba(0, 255, 0, 0.2);}")
        else:
            self.my_card_name.setStyleSheet("QLineEdit#my_card_name{background-color: rgba(255, 0, 0, 0.2);}")
    def validate_card_number(self, text):
        self.my_card_number.setText("".join(filter(str.isdigit, text)))
        if len(text) == 16:
            self.my_card_number.setStyleSheet("QLineEdit#my_card_number{background-color: rgba(0, 255, 0, 0.2);}")
        else:
            self.my_card_number.setStyleSheet("QLineEdit#my_card_number{background-color: rgba(255, 0, 0, 0.2);}")
    def validate_expiry(self, text):
        # This makes a slash appear after 2 numbers are entered
        if len(text) == 2 and text[2:3] != '/':
            text += '/'
            self.my_card_expiry.setText(text)
        # Check if text matches the desired format "MM/YY"
        if len(text) != 5 or text[2] != "/":
            # Independent Style sheet to change to the color red only aplicable to a certain line edit
            self.my_card_expiry.setStyleSheet("QLineEdit#my_card_expiry{background-color: rgba(255, 0, 0, 0.2);}")
        else:
            month_str, year_str = text[:2], text[3:]
            try:
                month, year = int(month_str), int(year_str)
            except ValueError:
                self.my_card_expiry.setStyleSheet("QLineEdit#my_card_expiry{background-color: rgba(255, 0, 0, 0.2);}")
                return
            # Check if month is between 1 and 12, and year is at least 24
            if month < 1 or month > 12 or year < 23:
                self.my_card_expiry.setStyleSheet("QLineEdit#my_card_expiry{background-color: rgba(255, 0, 0, 0.2);}")
            else:
                self.my_card_expiry.setStyleSheet("QLineEdit#my_card_expiry{background-color: rgba(0, 255, 0, 0.2);}")
    def eventFilter(self, source, event):
        # This checks for a backspace key and clears entire field
        # This is necessary as you cannot get rid of automatic slash
        # as it is permanent. Only way to do it:
        if (event.type() == QKeyEvent.KeyPress and event.key() == Qt.Key_Backspace):
            source.clear()
            return True
        return super().eventFilter(source, event)
    
    def validate_cvv(self, text):
        if len(text) == 3:
            self.my_card_cvv.setStyleSheet("QLineEdit#my_card_cvv{background-color: rgba(0, 255, 0, 0.2);}")
        else:
            self.my_card_cvv.setStyleSheet("QLineEdit#my_card_cvv{background-color: rgba(255, 0, 0, 0.2);}")
    # Button function to connect to sql
    def handle_payment_sql(self):
        try:
            cs = pyodbc.connect(
                "Driver={SQL Server};"
                "Server=COMPOOTER;"
                "Database=Transfer;"
                "Trusted_Connection=yes;"
            )

            print("Payment Connected")

            cursor = cs.cursor()

            cursor.execute("SELECT PaymentID FROM PaymentCounter")
            payment_id = cursor.fetchone()[0]

        
            name = self.my_card_name.text()
            card = self.my_card_number.text()
            expiry = self.my_card_expiry.text()
            cvv = self.my_card_cvv.text()
            if name == "" or card == "" or expiry == "" or cvv == "":
                cursor.close()
                cs.close()
            query = "INSERT INTO Payment (PaymentID, Name, Card, Expiry, CVV) VALUES (?,?,?,?,?)"
            my_values = (payment_id,name,card,expiry,cvv)
            cursor.execute(query,my_values)
            cursor.execute("UPDATE PaymentCounter SET PaymentID = PaymentID + 1")
            cs.commit()
            cursor.close()
            cs.close()
            
        except pyodbc.Error as e:
            print(e)
        
class ManageSeats(QWidget):
    def __init__(self,main_window):
        super(ManageSeats, self).__init__(main_window)

        self.my_main_window = main_window 
        formLayout = QFormLayout(self)
        formLayout.addRow("View Seats:", QSpinBox())
        self.setLayout(formLayout)

class ViewRevenue(QWidget):
    def __init__(self, main_window):
        super(ViewRevenue, self).__init__(main_window)
        layout = QFormLayout(self)

        my_graph1 = QRadioButton('Show 1 Revenue')
        my_graph2 = QRadioButton('Show 2 Revenue')
        my_graph3 = QRadioButton('Show 3 Revenue')
 

        self.my_show_group = QButtonGroup()
        self.my_show_group.addButton(my_graph1)
        self.my_show_group.addButton(my_graph2)
        self.my_show_group.addButton(my_graph3)
        self.my_show_group.buttonClicked.connect(self.handle_graph_show_clicked)

        my_group_box = QGroupBox()
        my_group_box.setLayout(QVBoxLayout())
        my_group_box.layout().addWidget(my_graph1)
        my_group_box.layout().addWidget(my_graph2)
        my_group_box.layout().addWidget(my_graph3)

        my_graph_title = QLabel("Pick a night to display a graph for:")
        layout.addRow(my_graph_title)
        layout.addRow(my_group_box)

        # create a figure and axis object
        self.fig, self.ax = plt.subplots(figsize=(8, 10), dpi=100)

        # add labels and title
        self.ax.set_xlabel("Seats Booked")
        self.ax.set_ylabel("Total Money")
        self.ax.set_title("Revenue:")

        # create a canvas to display the graph
        canvas = FigureCanvas(self.fig)
        layout.addRow("", canvas)
        self.setLayout(layout)

    def handle_graph_show_clicked(self, button):
        if button.text() == 'Show 1 Revenue':
            show = 1
        elif button.text() == 'Show 2 Revenue':
            show = 2
        else:
            show = 3

        try:
            cs = pyodbc.connect(
                "Driver={SQL Server};"
                "Server=COMPOOTER;"
                "Database=Transfer;"
                "Trusted_Connection=yes;"
            )

            print("Graph Connected")

            cursor = cs.cursor()

            # select the total number of seats for the specified show
            cursor.execute("SELECT SUM(Adult + Child + Elderly + Special) FROM Show WHERE ShowID = ?", (show,))
            total_seats = cursor.fetchone()[0]

            # select the number of seats sold for each ticket type for the specified show
            cursor.execute("SELECT SUM(Adult), SUM(Child), SUM(Elderly), SUM(Special) FROM Show WHERE ShowID = ?", (show,))
            adult_sold, child_sold, elderly_sold, special_sold = cursor.fetchone()

            # calculate the revenue for each ticket type
            adult_revenue = adult_sold * res.ticket_price_adult
            child_revenue = child_sold * res.ticket_price_child
            elderly_revenue = elderly_sold * res.ticket_price_elderly
            special_revenue = special_sold * res.ticket_price_special

            # calculate the total revenue
            total_revenue = adult_revenue + child_revenue + elderly_revenue + special_revenue

                # update the y-axis data to include the calculated revenue
            self.my_y = [adult_revenue, child_revenue, elderly_revenue, special_revenue, total_revenue]

                # update the x-axis data to include the total number of seats
            self.my_x = list(range(1, 6))

                # plot the data with the updated x- and y-axes
            self.ax.clear()
            self.ax.bar(self.my_x, self.my_y)
            self.ax.set_xlabel("Ticket Type")
            self.ax.set_ylabel("Revenue")
            self.ax.set_title("Revenue for Show {}".format(show))
            self.fig.canvas.draw_idle()

            cs.commit()
            cursor.close()
            cs.close()

        except pyodbc.Error as e:
            print(e)
class SearchCustomer(QWidget):
    def __init__(self,main_window):
        super(SearchCustomer, self).__init__(main_window)

        self.my_main_window = main_window 
        layout = QVBoxLayout(self)

        # create the search criteria combo box
        self.search_criteria_combo = QComboBox()
        self.search_criteria_combo.addItem("Filter by PaymentID (0 upwards)")
        self.search_criteria_combo.addItem("Filter by Show (1,2,3)")
        layout.addWidget(self.search_criteria_combo)

        # create the search term line edit
        self.search_term_edit = QLineEdit()
        layout.addWidget(self.search_term_edit)

        # create the search button
        self.search_button = QPushButton("Search")
        layout.addWidget(self.search_button)

        # create the results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(["Unique ID", "Name", "Card", "Seat"])
        layout.addWidget(self.results_table)

        self.setLayout(layout)

        # connect the search button clicked signal to the search function
        self.search_button.clicked.connect(self.search)

    def search(self):
        # get the selected search criteria and search term
        search_criteria = self.search_criteria_combo.currentText()
        search_term = self.search_term_edit.text()

        try:
            cs = pyodbc.connect(
                "Driver={SQL Server};"
                "Server=COMPOOTER;"
                "Database=Transfer;"
                "Trusted_Connection=yes;"
            )

            cursor = cs.cursor()

            if search_criteria == "Filter by PaymentID (0 upwards)":
                cursor.execute("SELECT Payment.PaymentID, Payment.Name, Payment.Card, Seats.SeatID "
                   "FROM Payment INNER JOIN Seats ON Payment.PaymentID = Seats.PaymentID "
                   "WHERE Payment.PaymentID = ?", (search_term,))
            elif search_criteria == "Filter by Show (1,2,3)":
                cursor.execute("SELECT Payment.PaymentID, Payment.Name, Payment.Card, Seats.SeatID "
                            "FROM Payment "
                            "INNER JOIN Seats ON Payment.PaymentID = Seats.PaymentID "
                            "WHERE Payment.PaymentID IN "
                            "(SELECT PaymentID FROM Show WHERE ShowID = ?)", (search_term,))

            # populate the results table with the query results
            results = cursor.fetchall()
            self.results_table.setRowCount(len(results))
            for i, row in enumerate(results):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    self.results_table.setItem(i, j, item)

            cursor.close()
            cs.close()

        except pyodbc.Error as e:
            print(e)

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
    
    my_qss_file_path = ""
    if sys.platform.startswith('win'):
        my_qss_file_path = "C:\\Users\\Vlad\\Desktop\\Transfer\\pyqt5 transfer\\src\\style.qss"
    else:
        my_qss_file_path = "./Transfer/pyqt5 transfer/src/style.qss"
    with open(my_qss_file_path, "r") as my_qss_file:
        _style = my_qss_file.read()
        my_app.setStyleSheet(_style)
    '''
    with open("C:\\Users\\Vlad\\Desktop\\Transfer\\pyqt5 transfer\\src\\style.qss", "r") as f:
        _style = f.read()
        my_app.setStyleSheet(_style)
    # Start the event loop.
    '''
    my_app.exec()
    #Your application won't reach here until you exit

if __name__ == "__main__":
    main()