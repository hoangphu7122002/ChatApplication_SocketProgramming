from tkinter import *
import tkinter
from tkinter.ttk import *

window = Tk()
window.title("Hoang Phu academic")
window.geometry("800x600")

#them label
lbl = tkinter.Label(window, text = "Hi main",fg = "red", font = ("Arial",58))
lbl.grid(column=0,row=0)

#them textbox
txt = Entry(window, width = 20)
txt.grid(column=0,row=1)

def handleButton():
    lbl.configure(text = "Hi" + txt.get())
    return 
def handleButton1():
    lbl.configure(text = "Hi" + combo.get())
    return 

#them button
btnHello = Button(window, text="Say Hello", command=handleButton)
btnHello.grid(column = 1, row = 2)

#them comboBox
combo = Combobox(window)
combo['values'] = ("hellas","huy","hoang phu")
combo.current(0)
combo.grid(column=0,row=2)

#them button
btnHello1 = Button(window,text="Say hello combo",command=handleButton1)
btnHello1.grid(column=1,row=2)

window.mainloop()
