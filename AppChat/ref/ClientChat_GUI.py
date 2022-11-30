from tkinter import *

Window = Tk()

def layout(name):
    # name = name
    # to show chat window

    Window.deiconify()
    Window.resizable(width=False,
                        height=False)
    Window.configure(width=470,
                        height=550,
                        bg="#17202A")

    labelHead = Label(Window,
                    bg="#17202A",
                    fg="#EAECEE",
                    text=name,
                    font="Helvetica 13 bold",
                    pady=5)
    labelHead.place(relwidth=1)

    line = Label(Window,width=450, bg="#ABB2B9")
    line.place(relwidth=1,rely=0.07,relheight=0.012)

    # Text console - show text message
    textCons = Text(Window,
                    width=20,
                    height=2,
                    bg="#17202A",
                    fg="#EAECEE",
                    font="Helvetica 14",
                    padx=5,
                    pady=5)
    textCons.place(relheight=0.745,
                    relwidth=1,
                    rely=0.08)
    textCons.config(cursor="arrow")
    textCons.config(state=DISABLED)

    labelBottom = Label(Window, bg="#ABB2B9", height=80)
    labelBottom.place(relwidth=1, rely=0.825)

    # The place for entering message
    entryMsg = Entry(labelBottom,
                    bg="#2C3E50",
                    fg="#EAECEE",
                    font="Helvetica 13")
    entryMsg.place(relwidth=0.74,
                    relheight=0.06,
                    rely=0.008,
                    relx=0.011)
    entryMsg.focus()

    # create a Send Button
    buttonMsg = Button(labelBottom,
                        text="Send",
                        font="Helvetica 10 bold",
                        width=20,
                        bg="#ABB2B9",
                        command=lambda: sendButton(entryMsg.get()))
    buttonMsg.place(relx=0.77,
                    rely=0.008,
                    relheight=0.06,
                    relwidth=0.22)

    # create a scroll bar
    scrollbar = Scrollbar(textCons)
    scrollbar.place(relheight=1,relx=0.974)
    scrollbar.config(command=textCons.yview)




    Window.mainloop()
    return

layout("Nguyen")
