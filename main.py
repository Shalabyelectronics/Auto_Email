from tkinter import *
from your_mail import YourMail

root = Tk()
root.geometry("+800+300")
root.title("Auto Mail Quotes V1.0")
root.iconbitmap("img/my.ico")
your_email_section = YourMail(root)
root.mainloop()