from tkinter import *
from tkinter import messagebox
import test_your_mail as tm
import json
import os

FONT = "Baloo Bhaijaan 2"
BACKGROUND_COLOR = "#F6F2D4"
FOREGROUND_COLOR = "#22577E"
LINES = "#95D1CC"
BORDER = "#5584AC"


class YourMail(Frame):
    def __init__(self, root):
        super().__init__()
        self.provider_smtp = None
        self.provider = None
        self.email_selected = None
        self.email_provider = None
        self.root = root
        self.save_password = None
        self.config(bg=BACKGROUND_COLOR, bd=5, pady=5, padx=15)
        self.your_section_l = Label(self, text="_Add your E-mail_", font=(FONT, 15, "bold"),
                                    fg=FOREGROUND_COLOR,
                                    bg=BACKGROUND_COLOR)
        self.pick_your_mail = Label(self, text="_pick your E-mail_", font=(FONT, 15, "bold"),
                                    fg=FOREGROUND_COLOR,
                                    bg=BACKGROUND_COLOR)
        self.your_first_name_l = Label(self, text="Your first name ", font=(FONT, 15), fg=FOREGROUND_COLOR,
                                       bg=BACKGROUND_COLOR)
        self.your_first_name_e = Entry(self, font=(FONT, 15, "bold"), fg="black", width=20, bg=LINES)
        self.your_last_name_l = Label(self, text="Your last name ", font=(FONT, 15), fg=FOREGROUND_COLOR,
                                      bg=BACKGROUND_COLOR)
        self.your_last_name_e = Entry(self, font=(FONT, 15, "bold"), fg="black", width=20, bg=LINES)
        self.save_button = Button(self, text="Save", width=25, font=(FONT, 15, "bold"), fg=FOREGROUND_COLOR,
                                  bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR, highlightthickness=0,
                                  command=self.save_your_email)
        self.your_email_l = Label(self, text="Your E-mail        ", font=(FONT, 15), fg=FOREGROUND_COLOR,
                                  bg=BACKGROUND_COLOR)
        self.your_email_e = Entry(self, font=(FONT, 15, "bold"), fg="black", width=20, bg=LINES)
        self.var = Variable()
        self.email_provider_google = Radiobutton(self, text="google.com", variable=self.var, value="@gmail.com",
                                                 bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR,
                                                 activebackground=BACKGROUND_COLOR, font=(FONT, 15),
                                                 command=self.complete_email)
        self.email_provider_yahoo = Radiobutton(self, text="yahoo.com", variable=self.var, value="@yahoo.com",
                                                bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR,
                                                activebackground=BACKGROUND_COLOR, font=(FONT, 15),
                                                command=self.complete_email)
        self.your_password_l = Label(self, text="Your password      ", font=(FONT, 15), fg=FOREGROUND_COLOR,
                                     bg=BACKGROUND_COLOR)
        self.password = StringVar()
        self.your_password_e = Entry(self, textvariable=self.password, show="*", font=(FONT, 15, "bold"), fg="black",
                                     width=20, bg=LINES)

        self.pick_your_email_list = Listbox(self, width=30, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR,
                                            font=(FONT, 15, "bold"))
        self.update_list_box()
        self.next_button = Button(self, text="Next Step", width=25, font=(FONT, 15, "bold"), fg=FOREGROUND_COLOR,
                                  bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR, highlightthickness=0,
                                  command=self.next_step)
        self.delete_email_b = Button(self, text="Delete E-mail", width=25, font=(FONT, 15, "bold"), fg=FOREGROUND_COLOR,
                                     bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR, highlightthickness=0,
                                     command=self.delete_email)

        self.delete_email_b.grid(column=1, row=6, pady=15)
        self.next_button.grid(column=2, row=6, pady=15)
        self.pick_your_email_list.grid(column=2, row=1, rowspan=5, padx=15)
        self.pick_your_mail.grid(column=2, row=0, columnspan=2)
        self.your_password_e.grid(column=1, row=5)
        self.your_password_l.grid(column=0, row=5, sticky=W)
        self.email_provider_yahoo.grid(column=1, row=4, sticky=W)
        self.email_provider_google.grid(column=0, row=4, sticky=W)
        self.your_email_e.grid(column=1, row=3)
        self.your_email_l.grid(column=0, row=3, sticky=W)
        self.your_section_l.grid(column=0, row=0, columnspan=2, sticky=N)
        self.save_button.grid(column=0, row=6, columnspan=1, pady=15, padx=20)
        self.your_last_name_e.grid(column=1, row=2, pady=5)
        self.your_last_name_l.grid(column=0, row=2, sticky=W)
        self.your_first_name_e.grid(column=1, row=1)
        self.your_first_name_l.grid(column=0, row=1, sticky=W)
        self.grid(column=0, row=0, pady=15, padx=15)

    def complete_email(self):
        your_email = self.your_email_e.get()
        if "@" in your_email:
            messagebox.showinfo(title="Attention",
                                message=f"your {your_email} include @ to apply auto fill remove it please.")
        elif your_email == "":
            messagebox.showinfo(title="Attention",
                                message="please don't leave it empty.")

        else:
            self.email_provider = self.var.get()
            self.your_email_e.delete(0, END)
            self.your_email_e.insert(0, your_email + self.email_provider)

    def save_your_email(self):
        self.check_smtp()
        new_data = {
            self.your_email_e.get(): {
                "first name": self.your_first_name_e.get().title(),
                "last name": self.your_last_name_e.get().title(),
                "password": self.password.get(),
                "smtp": self.provider_smtp  # check provider first to decide which will be added
            }
        }
        if len(self.your_email_e.get()) == 0 and len(self.your_first_name_e.get()) == 0 and len(
                self.your_last_name_e.get()) == 0:
            messagebox.showinfo(title="Attention",
                                message="please don't leave email and your first , last name empty")
        elif len(self.password.get()) < 8:
            messagebox.showinfo(title="Attention",
                                message=f"please check your password as it is {len(self.password.get())} length and "
                                        f"it's not correct, be sure it is at least 8 digits length.")
        else:
            if os.path.isfile("data/your_data.json"):
                with open("data/your_data.json") as data_file:
                    data = json.load(data_file)
                    if self.your_email_e.get() in data:
                        messagebox.showinfo(title="Attention",
                                            message=f"Your {self.your_email_e.get()} is already existed.")
                        self.clear_all_entries()
                    else:
                        with open("data/your_data.json", "r") as read_data_file:
                            data = json.load(read_data_file)
                            data.update(new_data)
                        with open("data/your_data.json", "w") as update_data_file:
                            json.dump(data, update_data_file, indent=4)
                        messagebox.showinfo(title="Attention",
                                            message=f"Your {self.your_email_e.get()} added successfully.")
                        self.pick_your_email_list.insert(END, self.your_email_e.get())
                        self.save_password = self.password.get()
                        self.clear_all_entries()

            else:
                with open("data/your_data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
                messagebox.showinfo(title="Attention",
                                    message=f"Your {self.your_email_e.get()} added successfully.")
                self.pick_your_email_list.insert(END, self.your_email_e.get())
                self.save_password = self.password.get()
                self.clear_all_entries()

    def clear_all_entries(self):
        self.your_first_name_e.delete(0, END)
        self.your_last_name_e.delete(0, END)
        self.your_email_e.delete(0, END)
        self.your_password_e.delete(0, END)

    def update_list_box(self):
        if os.path.isfile("data/your_data.json"):
            with open("data/your_data.json", "r") as data_file:
                data = json.load(data_file)
            for email in data:
                self.pick_your_email_list.insert(END, email)

    def next_step(self):
        self.email_selected = self.pick_your_email_list.get(ANCHOR)
        try:
            with open("data/your_data.json", "r") as data_file:
                data = json.load(data_file)
                self.save_password = data[self.email_selected]["password"]
        except KeyError:
            messagebox.showinfo(title="Attention",
                                message=f"You  did not select any email yet..")
        else:
            if len(self.email_selected) > 0:
                self.destroy()
                tm.SetupEmail(root=self.root, your_email=self.email_selected, password=self.save_password)
            else:
                messagebox.showinfo(title="Attention",
                                    message=f"Your did not select any email yet..")

    def delete_email(self):
        self.email_selected = self.pick_your_email_list.get(ANCHOR)
        with open("data/your_data.json", "r") as data_file:
            data = json.load(data_file)
            if self.email_selected in data:
                ask_y_n = messagebox.askyesno(title="Deletion Confirmation", message=f"Are you sure that you want to "
                                                                                     f"delete {self.email_selected}")
                if ask_y_n:
                    del data[self.email_selected]
                    data.update(data_file)
                    self.pick_your_email_list.delete(ANCHOR)
            else:
                messagebox.showinfo(title="Attention",
                                    message=f"You  did not select any your email yet..")

        with open("data/your_data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)

    def check_smtp(self):
        provider = []
        for char in range(len(self.your_email_e.get())):
            if self.your_email_e.get()[char] == "@":
                for dot in self.your_email_e.get()[char + 1:]:
                    if dot == ".":
                        break
                    else:
                        provider.append(dot)
        self.provider = "".join(provider).title()
        if self.provider == "Gmail":
            self.provider_smtp = "smtp.gmail.com"
        elif self.provider == "Yahoo":
            self.provider_smtp = "smtp.mail.yahoo.com"
        else:
            messagebox.showinfo(title="Attention",
                                message=f"You  do not know what is your email smtp server")
