from tkinter import *
# defining login function


def login():
    # getting form data
    name = username.get()
    password = pwd.get()
    p2p_server_addr = IPv4.get()
    # applying empty validation
    if name == '' or password == '':
        message.set("fill the empty field!!!")
    else:
        if name == "GiaPhong" and password == "123":
            message.set("Login Succes")
        elif name == "HoangPhu" and password == "123":
            message.set("Login Succes")
        elif name == "DacLoc" and password == "123":
            message.set("Login Succes")
        elif name == "NguyenTruong" and password == "123":
            message.set("Login Succes")
        else:
            message.set("Wrong name or password!!!")
# defining login form function


def Loginform():
    global login_screen
    login_screen = Tk()
    # Setting title of screen
    login_screen.title("Login Form")
    # setting height and width of screen
    login_screen.geometry("300x250")
    # declaring variable
    global message
    global username
    global pwd
    global IPv4
    username = StringVar()
    pwd = StringVar()
    IPv4 = StringVar()
    message = StringVar()
    # Creating layout of login form
    Label(login_screen, width="300", text="Please enter details below",
          bg="orange", fg="white").pack()
    # name Label
    Label(login_screen, text="Username").place(x=20, y=40)
    # name textbox
    Entry(login_screen, textvariable=username).place(x=90, y=42)
    # pwd Label
    Label(login_screen, text="password").place(x=20, y=80)
    # pwd textbox
    Entry(login_screen, textvariable=pwd, show="*").place(x=90, y=82)
    # Label for displaying login status[success/failed]

    Label(login_screen, text="Server IPv4").place(x=20, y=120)
    # name textbox
    Entry(login_screen, textvariable=IPv4).place(x=90, y=122)
    # pwd Label

    Label(login_screen, text="", textvariable=message).place(x=80, y=180)
    # Login button

    Button(login_screen, text="Login", width=10, height=1,
           bg="orange", command=login).place(x=105, y=150)

    login_screen.mainloop()
