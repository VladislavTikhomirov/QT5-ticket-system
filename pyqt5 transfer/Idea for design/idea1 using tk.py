#import the necessary libraries
import tkinter as tk
from tkinter import ttk

#create a window object
root = tk.Tk()

#define a function to open the second window
def open_window2():
    window2 = tk.Toplevel(root)
    window2.title("Window 2")
    window2.geometry("300x300")
    window2.configure(bg="#f8f8f8")

#define a function to open the third window
def open_window3():
    window3 = tk.Toplevel(root)
    window3.title("Window 3")
    window3.geometry("300x300")
    window3.configure(bg="#f8f8f8")

#define a function to open the fourth window
def open_window4():
    window4 = tk.Toplevel(root)
    window4.title("Window 4")
    window4.geometry("300x300")
    window4.configure(bg="#f8f8f8")

#define a function to open the fifth window
def open_window5():
    window5 = tk.Toplevel(root)
    window5.title("Window 5")
    window5.geometry("300x300")
    window5.configure(bg="#f8f8f8")

#define a function to open the sixth window
def open_window6():
    window6 = tk.Toplevel(root)
    window6.title("Window 6")
    window6.geometry("300x300")
    window6.configure(bg="#f8f8f8")

#create a frame to hold the buttons
frame = tk.Frame(root, bg="#f8f8f8")
frame.pack()

#create buttons to open each window
button1 = ttk.Button(frame, text="Window 2", command=open_window2)
button1.pack()

button2 = ttk.Button(frame, text="Window 3", command=open_window3)
button2.pack()

button3 = ttk.Button(frame, text="Window 4", command=open_window4)
button3.pack()

button4 = ttk.Button(frame, text="Window 5", command=open_window5)
button4.pack()

button5 = ttk.Button(frame, text="Window 6", command=open_window6)
button5.pack()

#run the window
root.mainloop()
