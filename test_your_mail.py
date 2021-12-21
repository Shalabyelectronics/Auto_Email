import smtplib
from tkinter import *
import your_mail as ym
from tkinter import messagebox
import recipient_email as rm
import webbrowser

FONT = "Baloo Bhaijaan 2"
BACKGROUND_COLOR = "#F6F2D4"
FOREGROUND_COLOR = "#22577E"
LINES = "#95D1CC"
BORDER = "#5584AC"


class SetupEmail(Frame):
    def __init__(self, root, your_email, password):
        super().__init__()
        self.root = root
        self.config(bg=BACKGROUND_COLOR, bd=5, pady=5, padx=15)
        self.your_email = your_email
        self.password = password
        self.provider = None
        self.provider_smtp = None
        self.provider_port = [465, 587]
        self.help_site = None
        self.is_pass = False
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
        self.steps_list = Listbox(self, width=30, height=8, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR,
                                  font=(FONT, 15, "bold"), borderwidth=5, relief="sunken")
        self.test_connection = Button(self, text="Test your connection", width=10, font=(FONT, 15, "bold"),
                                      fg=FOREGROUND_COLOR,
                                      bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR, highlightthickness=0,
                                      command=self.test_connection)
        self.test_result = Label(self, text="", font=(FONT, 15, "bold"), fg="red",
                                 bg=BACKGROUND_COLOR, relief="flat")
        self.next_button = Button(self, text="Next Step", width=25, font=(FONT, 15, "bold"), fg=FOREGROUND_COLOR,
                                  bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR, highlightthickness=0,
                                  command=self.go_next)
        self.help_button = Button(self, text="More details about setting up your e-mail.", width=25,
                                  font=(FONT, 15, "bold"), fg=FOREGROUND_COLOR,
                                  bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR, highlightthickness=0,
                                  command=self.get_help)
        self.back_button = Button(self, text="Go back", width=25, font=(FONT, 15, "bold"), fg=FOREGROUND_COLOR,
                                  bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR, highlightthickness=0,
                                  command=self.back_to)

        self.feed_info()

        self.test_result.grid(column=0, row=6, columnspan=4, sticky=W + E, pady=15)
        self.test_connection.grid(column=0, row=5, columnspan=4, sticky=W + E, pady=15)
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
            self.email_provider_e.configure(state="disabled")
            self.email_provider_l.configure(text=f"{self.provider} SMTP :")
            self.steps_list.insert(0, " 1- Open your Google Admin console ")
            self.steps_list.insert(1, " (admin.google.com).")
            self.steps_list.insert(2, " 2- Click Security > Basic settings.")
            self.steps_list.insert(3, " 3-Under Less secure apps, select Go to")
            self.steps_list.insert(4, " settings for less secure apps..")
            self.steps_list.insert(5, " 4-In the subwindow, select the Enforce "
                                      "radio button.")
            self.steps_list.insert(6, " access to less secure apps for all users.")
            self.steps_list.insert(7, " 5- Click the Save button.")
            self.help_site = "https://support.google.com/accounts/answer/6010255?hl=en"
        elif self.provider == "Yahoo":
            self.provider_smtp = "smtp.mail.yahoo.com"
            self.email_provider_e.insert(0, self.provider_smtp)
            self.email_provider_e.configure(state="disabled")
            self.email_provider_l.configure(text=f"{self.provider} SMTP :")
            self.steps_list.insert(0, " 1- Log in to Yahoo mailbox and go to ")
            self.steps_list.insert(1, " Account Info page.")
            self.steps_list.insert(2, " 2-Choose Account Security and turn on")
            self.steps_list.insert(3, " the button of Allow apps that use ")
            self.steps_list.insert(4, " less secure sign in.")
            self.steps_list.insert(5, " 3-access to less secure apps ")
            self.steps_list.insert(6, " for all users.")
            self.help_site = "https://help.yahoo.com/kb/SLN27791.html"
        else:
            self.provider_smtp = f"Add your {self.provider} SMTP."
            self.description_l.configure(text=f"Your {self.provider} provider did not updated yet.")
            self.email_provider_l.configure(text=f"{self.provider} SMTP :")
            self.email_provider_e.insert(0, self.provider_smtp)
            self.help_site = "https://google.com"

    def test_connection(self):
        try:
            with smtplib.SMTP(self.provider_smtp, port=587) as connection:
                connection.starttls()
                connection.login(user=self.your_email, password=self.password)
                connection.sendmail(from_addr=self.your_email, to_addrs=self.your_email, msg="Subject: Hello, "
                                                                                             "World\n\n "
                                                                                             "We are testing the email "
                                                                                             "connection.")
                connection.close()
        except EXCEPTION as e:
            self.test_result.config(text="Your E-mail is not ready please be sure to follow the steps.")
            self.help_button.grid(column=0, row=7, columnspan=4, sticky=W + E, pady=15)
            self.back_button.grid(column=0, row=8, columnspan=4, sticky=W + E, pady=15)
            print(e)
        else:
            self.test_result.config(text="Your E-mail is ready.")
            self.next_button.grid(column=0, row=7, columnspan=4, sticky=W + E, pady=15)
            self.is_pass = True

    def back_to(self):
        self.destroy()
        ym.YourMail(self.root)

    def get_help(self):
        webbrowser.open(self.help_site, new=1)

    def go_next(self):
        if self.is_pass:
            self.destroy()
            rm.RecipientEmail(self.root)
        else:
            messagebox.showinfo(title="Attention",
                                message=f"You  did not test your email yet..")
