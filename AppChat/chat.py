from tkinter import *

# GUI


# Send function
# def send():
#     global chat_message
#     global txt
#     global msg

#     msg = chat_message.get()
#     print(msg)
#     txt.insert(END, "\n" + msg)


def prepareMessage():
    global root
    global chat_message
    global txt
    global msg

    root = Tk()
    root.title("Chatbot")
    BG_GRAY = "#ABB2B9"
    BG_COLOR = "#17202A"
    TEXT_COLOR = "#EAECEE"
    FONT = "Helvetica 14"
    FONT_BOLD = "Helvetica 13 bold"

    chat_message = StringVar()

    # chat_message.delete(0, END)

    Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10, width=20, height=1).grid(
        row=0)

    txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
    txt.grid(row=1, column=0, columnspan=2)

    scrollbar = Scrollbar(txt)
    scrollbar.place(relheight=1, relx=0.974)

    Entry(root, bg="#2C3E50", fg=TEXT_COLOR,
          font=FONT, width=55, textvariable=chat_message).grid(row=2, column=0)

    Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY,
           command=send).grid(row=2, column=1)

    # txt.insert(END, '\n' + chat_message)

    root.mainloop()
