import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QLineEdit
from PyQt5.QtGui import QColor, QPalette, QFont
from PyQt5 import QtCore, QtGui

class seatmap(QWidget):
    def __init__(self,width,height,night):
        super().__init__()
        self.width = width
        self.height = height
        self.night = night
        self.selected_seats = []
        self.CreateUI()
    def CreateUI(self):
        self.setWindowTitle(str(self.night))
        self.seatspicked = QLineEdit()
        self.price_of_seats = QLineEdit()
        self.price_of_seats.setPlaceholderText("Price: £")
        
        
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor('#dda83e'))
        self.setPalette(palette)
        # Create a horizontal layout for the label and buttons
        hbox = QHBoxLayout()
        # Create a black frame for the left-hand side
        black_frame = QFrame()
        black_frame.setFixedWidth(80) # Set a fixed width of 80 pixels
        black_frame.setStyleSheet('background-color: black')
        screen_label = QLabel('Screen')
        screen_label.setStyleSheet('color: white')
        screen_label.setAlignment(QtCore.Qt.AlignCenter)
        vbox = QVBoxLayout()
        vbox.addWidget(screen_label)
        black_frame.setLayout(vbox)
        hbox.addWidget(black_frame)
        # Create a white frame for the seats
        white_frame = QFrame()
        white_frame.setFixedWidth(620) # Set a fixed width of 620 pixels
        white_frame.setFrameShape(QFrame.Box)
        white_frame.setStyleSheet('background-color: white')
        hbox.addWidget(white_frame)
        # Create a vertical layout for the buttons
        vbox2 = QVBoxLayout()
        for i in range(1,21):
            hbox3 = QHBoxLayout()
            for j in range(1,11):
                button = QPushButton(chr(96+j).upper() + str(i))
                button.setStyleSheet('background-color: grey')
                button.setFixedSize(40, 40)
                font = QFont()
                font.setPointSize(8)
                button.setFont(font)
                button.clicked.connect(self.toggle_color)
                button.clicked.connect(self.update_selected_seats)
                hbox3.addWidget(button)
            vbox2.addLayout(hbox3)
        # Add the vertical layout to the white frame
        white_frame.setLayout(vbox2)
        # Create a white frame for the right-hand side
        white_frame_r = QFrame()
        white_frame_r.setFixedWidth(300)
        white_frame_r.setFixedHeight(300)
        white_frame_r.setFrameShape(QFrame.Box)
        white_frame_r.setStyleSheet('background-color: white')
        # Create a vertical layout for the white frame
        vbox3 = QVBoxLayout()
        # Add a label to the layout
        screen_label2 = QLabel('Seats Selected:')
        screen_label2.setStyleSheet('color: Black')
        screen_label2.setFont(QFont('Arial',16))
        screen_label2.setAlignment(QtCore.Qt.AlignLeft)
        vbox3.addWidget(screen_label2)
        # Add the line edit to the layout with AlignTop alignment                          ---------------------------->>>> LINE EDIT HERE <<<<------------------------------
        self.seatspicked = QLineEdit()
        self.seatspicked.setReadOnly(True)
        self.seatspicked.setAlignment(QtCore.Qt.AlignTop)
        font = QFont()
        font.setBold(True)
        self.seatspicked.setFont(QFont('Arial', 16)) # set the font size to 16
        self.seatspicked.setFixedHeight(50) # set the height to 50 
        self.seatspicked.setStyleSheet("border: 1px solid black;")        
        vbox3.addWidget(self.seatspicked)     
        # Create the confirm button
        self.confirm_button = QPushButton('Confirm')
        self.confirm_button.setStyleSheet('background-color: #131f44; color: #131f44; border-radius: 5px; padding: 10px; font-size: 18px;')
        self.confirm_button.setStyleSheet('QPushButton:hover { background-color: #1a2a5a; }')
        self.confirm_button.setFixedSize(120, 40)
        # Connect the clicked signal of the confirm button to the quit slot of QApplication
        #self.confirm_button.clicked.connect(self.update_seats_sql)
        self.confirm_button.clicked.connect(self.closeApp)
        # Create a horizontal layout for the confirm button
        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.confirm_button)
        hbox4.setAlignment(QtCore.Qt.AlignRight)
        # Add the horizontal layout to the vertical layout for the right-hand frame
        vbox3.addLayout(hbox4)
        # Set the vertical alignment of the layout to AlignTop
        vbox3.setAlignment(QtCore.Qt.AlignTop)
        # Set the layout of the right-hand frame
        white_frame_r.setLayout(vbox3)
        # Add the right-hand frame to the horizontal layout
        hbox.addWidget(white_frame_r)
        # Center the layout horizontally
        hbox.setContentsMargins(40, 0, 40, 0)
        hbox.setAlignment(QtCore.Qt.AlignCenter)
        # Set the main layout of the window to the horizontal layout
        self.setLayout(hbox)

    def toggle_color(self):
        button = self.sender()
        if button.styleSheet() == 'background-color: grey':
            button.setStyleSheet('background-color: green')
            self.selected_seats.append(button.text()) # Add the selected seat to the list
            self.selected_seats.sort()
        else:
            button.setStyleSheet('background-color: grey')
            self.selected_seats.remove(button.text()) # Remove the deselected seat from the list
        #print('Selected seats:', self.selected_seats) # Print the selected seats to the console
    def update_selected_seats(self):
        seats_picked = str(self.selected_seats)
        seats_picked = seats_picked[1:-1]  # removes the first and last characters (i.e. '[' and ']')
        self.seatspicked.setText(seats_picked)
    def closeApp(self):
        self.close()
    def update_seats_sql(self):
        cs = (
        "Driver = {SQL Server}"
        "Server=svr-cmp-01"
        "Database=22TikhomirV699"
        "Trusted_Connection=yes"
        "UTD=COLLYERS\22TikhomirV699"
        ) 
        mycursor = cs.cursor()
        for i in range(0, len(self.selected_seats)):   
            mycursor.execute("SELECT * FROM Seats WHERE ButtonID="+i)
            if mycursor.fetchone():
                print("Button exists")
            else:
                print("Nope")
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.exit(app.exec_())





        


