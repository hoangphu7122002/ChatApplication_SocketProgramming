from tkinter import *

Window = Tk()

def func():
    print("Clicked")
    return

def main_layout(clients):
    Window.deiconify()
    Window.title("CHATROOM")
    Window.resizable(width=False,
                        height=False)
    Window.configure(width=470,
                        height=550,
                        bg="#17202A")

    mainHead = Label(Window,
                    bg="#17202A",
                    fg="#EAECEE",
                    text="Chat app",
                    font="Helvetica 13 bold",
                    pady=5,
                    justify=CENTER)
    mainHead.place(relwidth=1)

    client_show = Text(Window,
                        width=20,
                        height=2,
                        bg="#ffffff",
                        fg="#EAECEE",
                        font="Helvetica 14",
                        padx=5,
                        pady=5)
    client_show.place(relheight=1,
                    relwidth=1,
                    rely=0.08)
    client_show.config(state=DISABLED, cursor="arrow")
    
    # Scroll bar
    scrollbar = Scrollbar(Window, command=client_show.yview)
    scrollbar.place(relheight=1,
                    relwidth=1,
                    rely=0.08,
                    relx=0.95)
    client_show.configure(yscrollcommand = scrollbar.set)
    
    # client_show.tag_configure("tag_name", justify="center")
    # Client show on the home page
    client_show.config(state=NORMAL)
    for i in range(10):
        client = Label(client_show, width = 60, height=4, bg="#3c4043", text=f"Client {i}", justify=LEFT)
        client_show.window_create("end", window=client)
        client.bind("<Button-1>", lambda e: func())
        client_show.insert("end","\n")
        client_show.insert("end","\n")
    # for client in clients:
    #     client_name = client
    Window.mainloop()

main_layout(1)