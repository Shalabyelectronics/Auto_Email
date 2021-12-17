from tkinter import *
from your_mail import YourMail, FOREGROUND_COLOR

root = Tk()
root.geometry("+800+100")
root.config(bg=FOREGROUND_COLOR)
root.title("Auto Mail Quotes V1.0")
root.iconbitmap("img/my.ico")
your_email_section = YourMail(root)
root.mainloop()
