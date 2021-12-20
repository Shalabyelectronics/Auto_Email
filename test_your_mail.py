from tkinter import *
import webbrowser
import smtplib as sm
from tkinter import messagebox
import json
import os

FONT = "Baloo Bhaijaan 2"
BACKGROUND_COLOR = "#F6F2D4"
FOREGROUND_COLOR = "#22577E"
LINES = "#95D1CC"
BORDER = "#5584AC"


class SetupEmail(Frame):
    def __init__(self, root, your_email):
        super().__init__()
        self.root = root
        self.config(bg=BACKGROUND_COLOR, bd=5, pady=5, padx=15)
        self.your_email = your_email
        self.provider = None
        self.provider_smtp = None
        self.provider_port = [465, 587]
        self.description_l = Label(self, text=f"Now we are going to get {self.your_email} ready.",
                                   font=(FONT, 15, "bold"),
                                   fg=FOREGROUND_COLOR,
                                   bg=BACKGROUND_COLOR)
        self.email_provider_l = Label(self, text=f"{self.provider} SMTP :", font=(FONT, 15, "bold"),
                                      fg=FOREGROUND_COLOR,
                                      bg=BACKGROUND_COLOR)
        self.email_provider_e = Entry(self, font=(FONT, 15, "bold"), fg="black", width=20, bg=LINES, justify="center")
        self.email_port_l = Label(self, text=f"Port      :", font=(FONT, 15, "bold"), fg=FOREGROUND_COLOR,
                                  bg=BACKGROUND_COLOR)
        self.email_port_e = Entry(self, font=(FONT, 15, "bold"), fg="black", width=20, bg=LINES, justify="center")
        self.email_port_e.insert(0, f"{self.provider_port[0]} or {self.provider_port[1]}")
        self.email_port_e.configure(state="disabled")
        self.how_to_l = Label(self,
                              text=f"You need to turning on 'less secure apps' \nsettings as mail domain Administrator.",
                              font=(FONT, 15, "bold"),
                              fg=FOREGROUND_COLOR,
                              bg=BACKGROUND_COLOR, borderwidth=10, relief="sunken")
        self.steps_l = Label(self, text="Steps", font=(FONT, 15, "bold"), fg=FOREGROUND_COLOR,
                             bg=BACKGROUND_COLOR)
        self.steps_list = Listbox(self, width=30, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR,
                                  font=(FONT, 15, "bold"), borderwidth=5, relief="sunken")
        self.steps_list.insert(0, " 1- Open your Google Admin console ")
        self.steps_list.insert(1, " (admin.google.com).")
        self.steps_list.insert(2, " 2- Click Security > Basic settings.")
        self.steps_list.insert(3, " 3-Under Less secure apps, select Go to")
        self.steps_list.insert(4, " settings for less secure apps..")
        self.steps_list.insert(5, " 4- In the subwindow, select the Enforce access to less secure apps for all users "
                                  "radio button.")
        self.steps_list.insert(6, " 4- In the subwindow, select the Enforce access to less secure apps for all users "
                                  "radio button.")
        self.steps_list.insert(4," 5- (You can also use the Allow users to manage their access to less secure apps, "
                                 "but don't forget to turn on the less secure apps option in users settings then!)")
        self.steps_list.insert(5, " 6- Click the Save button.")


        self.feed_info()
        self.steps_list.grid(column=2, row=1, columnspan=2, rowspan=4, padx=15)
        self.steps_l.grid(column=2, row=0, columnspan=2)
        self.how_to_l.grid(column=0, row=3, columnspan=2)
        self.email_port_e.grid(column=1, row=2, sticky=W, pady=15)
        self.email_port_l.grid(column=0, row=2, sticky=W)
        self.email_provider_e.grid(column=1, row=1, sticky=W, pady=15)
        self.email_provider_l.grid(column=0, row=1, sticky=W)
        self.description_l.grid(column=0, row=0, columnspan=2)
        self.grid(column=0, row=0, pady=15, padx=15)

    def feed_info(self):
        provider = []
        for char in range(len(self.your_email)):
            if self.your_email[char] == "@":
                for dot in self.your_email[char + 1:]:
                    if dot == ".":
                        break
                    else:
                        provider.append(dot)
        self.provider = "".join(provider).title()
        if self.provider == "Gmail":
            self.provider_smtp = "smtp.gmail.com"
            self.email_provider_e.insert(0, self.provider_smtp)
            self.email_provider_l.configure(text=f"{self.provider} SMTP :")
        elif self.provider == "Yahoo":
            self.provider_smtp = "smtp.mail.yahoo.com"
            self.email_provider_e.insert(0, self.provider_smtp)
            self.email_provider_e.configure(state="disabled")
            self.email_provider_l.configure(text=f"{self.provider} SMTP :")
        else:
            self.provider_smtp = f"Add your {self.provider} SMTP."
            self.description_l.configure(text=f"Your {self.provider} provider did not updated yet.")
            self.email_provider_l.configure(text=f"{self.provider} SMTP :")
            self.email_provider_e.insert(0, self.provider_smtp)


'''
 Turning on 'less secure apps' settings as mail domain Administrator

Open your Google Admin console (admin.google.com).
Click Security > Basic settings.
Under Less secure apps, select Go to settings for less secure apps.
In the subwindow, select the Enforce access to less secure apps for all users radio button.
(You can also use the Allow users to manage their access to less secure apps, but don't forget to turn on the less secure apps option in users settings then!)
Click the Save button.
'''
