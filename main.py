from tkinter import *
import your_mail as ym
import send_email_step as ses

FOREGROUND_COLOR = "#22577E"

root = Tk()
root.geometry("+500+50")
root.resizable(False, False)
root.config(bg=FOREGROUND_COLOR)
root.title("Auto Mail Quotes V1.0")
root.iconbitmap("img/my.ico")
ses.SendEmail(root, from_email="tsending4@gmail.com", to_email="dddd@outlook.com")
# ym.YourMail(root)
root.mainloop()
