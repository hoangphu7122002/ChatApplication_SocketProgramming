def sendFileUI():
    chatClient.withdraw()
    sendFileWindow = Toplevel()
    sendFileWindow.config(height=60, width=450)
    # The place for entering message
    entryFilePath = Entry(sendFileWindow,
                          bg="#2C3E50",
                          fg="#EAECEE",
                          font="Helvetica 13")
    entryFilePath.place(relwidth=0.55,
                        relheight=0.8,
                        rely=0.008,
                        relx=0.21)
    entryFilePath.focus()

    # create a Send Button
    buttonFile = Button(sendFileWindow,
                        text="Send",
                        font="Helvetica 10 bold",
                        width=10,
                        bg="#ABB2B9",
                        command=lambda: print()) # Change this function

    buttonFile.place(relx=0.77,
                      rely=0.008,
                      relheight=0.8,
                      relwidth=0.197)


    # create a exit Button
    buttonExit = Button(sendFileWindow,
                        text="<-",
                        font="Helvetica 10 bold",
                        width=10,
                        bg="#ABB2B9",
                        command=lambda: print()) # Change this function
    buttonExit.place(relx=0,
                      rely=0.008,
                      relheight=0.8,
                      relwidth=0.197)