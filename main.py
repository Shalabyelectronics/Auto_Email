import recipient_email as rm
from tkinter import *
from your_mail import YourMail, FOREGROUND_COLOR


root = Tk()
root.geometry("+700+50")
root.resizable(False, False)
root.config(bg=FOREGROUND_COLOR)
root.title("Auto Mail Quotes V1.0")
root.iconbitmap("img/my.ico")
rm.RecipientEmail(root)
root.mainloop()
