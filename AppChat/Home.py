# Import Required Module
from tkinter import *
from tkinter.ttk import *

# Create Root Object


def homeLayout():

    root = Tk()
    # Set Geometry(widthxheight)
    root.title("Hello")
    root.geometry('500x500')

    # Create style Object
    style = Style()

    style.configure('TButton', font=('calibri', 20, 'bold'),
                    borderwidth='4')

    # Changes will be reflected
    # by the movement of mouse.
    style.map('TButton', foreground=[('active', '!disabled', 'green')],
              background=[('active', 'black')])

    # button 1
    btn1 = Button(root, text='Show Peers')
    btn1.grid(row=0, column=1, padx=50)

    # button 2
    btn2 = Button(root, text='Group', command=None)
    btn2.grid(row=0, column=2, pady=10)

    # Execute Tkinter
    root.mainloop()


homeLayout()
