import os
from tkinter import *
from your_mail import YourMail, FOREGROUND_COLOR
from test_your_mail import SetupEmail

root = Tk()
root.geometry("+700+50")
root.resizable(False, False)
root.config(bg=FOREGROUND_COLOR)
root.title("Auto Mail Quotes V1.0")
root.iconbitmap("img/my.ico")
# your_email_section = YourMail(root)
set_up = SetupEmail(root,"mom@yahoo.com")

root.mainloop()

