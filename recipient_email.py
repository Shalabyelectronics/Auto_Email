from tkinter import *
from tkinter import messagebox
import json
import os

FONT = "Baloo Bhaijaan 2"
BACKGROUND_COLOR = "#F6F2D4"
FOREGROUND_COLOR = "#22577E"
LINES = "#95D1CC"
BORDER = "#5584AC"


class RecipientEmail(Frame):
    def __init__(self, root):
        super().__init__()
        self.email_provider = None
        self.email_selected = None
        self.root = root
        self.config(bg=BACKGROUND_COLOR, bd=5, pady=5, padx=15)
        self.recipient_section_l = Label(self, text="_Add recipient E-mail_", font=(FONT, 15, "bold"),
                                         fg=FOREGROUND_COLOR,
                                         bg=BACKGROUND_COLOR)
        self.pick_recipient_mail = Label(self, text="_Recipients E-mail_", font=(FONT, 15, "bold"),
                                         fg=FOREGROUND_COLOR,
                                         bg=BACKGROUND_COLOR)
        self.recipient_first_name_l = Label(self, text="Recipient first name ", font=(FONT, 15), fg=FOREGROUND_COLOR,
                                            bg=BACKGROUND_COLOR)
        self.recipient_first_name_e = Entry(self, font=(FONT, 15, "bold"), fg="black", width=20, bg=LINES)
        self.recipient_last_name_l = Label(self, text="Recipient last name ", font=(FONT, 15), fg=FOREGROUND_COLOR,
                                           bg=BACKGROUND_COLOR)
        self.recipient_last_name_e = Entry(self, font=(FONT, 15, "bold"), fg="black", width=20, bg=LINES)
        self.save_button = Button(self, text="Save", width=25, font=(FONT, 15, "bold"), fg=FOREGROUND_COLOR,
                                  bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR, highlightthickness=0,
                                  command=self.save_recipient_email)
        self.recipient_email_l = Label(self, text="recipient E-mail    ", font=(FONT, 15), fg=FOREGROUND_COLOR,
                                       bg=BACKGROUND_COLOR)
        self.recipient_email_e = Entry(self, font=(FONT, 15, "bold"), fg="black", width=20, bg=LINES)
        self.var = Variable()
        self.email_provider_google = Radiobutton(self, text="google.com", variable=self.var, value="@gmail.com",
                                                 bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR,
                                                 activebackground=BACKGROUND_COLOR, font=(FONT, 15),
                                                 command=self.complete_email)
        self.email_provider_yahoo = Radiobutton(self, text="yahoo.com", variable=self.var, value="@yahoo.com",
                                                bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR,
                                                activebackground=BACKGROUND_COLOR, font=(FONT, 15),
                                                command=self.complete_email)
        self.email_provider_hotmail = Radiobutton(self, text="hotmail.com", variable=self.var, value="@hotmail.com",
                                                  bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR,
                                                  activebackground=BACKGROUND_COLOR, font=(FONT, 15),
                                                  command=self.complete_email)
        self.email_provider_outlook = Radiobutton(self, text="outlook.com", variable=self.var, value="@outlook.com",
                                                  bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR,
                                                  activebackground=BACKGROUND_COLOR, font=(FONT, 15),
                                                  command=self.complete_email)

        self.pick_recipient_email_list = Listbox(self, width=30, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR,
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
        self.pick_recipient_email_list.grid(column=2, row=1, rowspan=5, padx=15)
        self.pick_recipient_mail.grid(column=2, row=0, columnspan=2)
        self.email_provider_yahoo.grid(column=1, row=4, sticky=W)
        self.email_provider_google.grid(column=0, row=4, sticky=W)
        self.email_provider_hotmail.grid(column=1, row=5, sticky=W)
        self.email_provider_outlook.grid(column=0, row=5, sticky=W)
        self.recipient_email_e.grid(column=1, row=3)
        self.recipient_email_l.grid(column=0, row=3, sticky=W)
        self.recipient_section_l.grid(column=0, row=0, columnspan=2, sticky=N)
        self.save_button.grid(column=0, row=6, columnspan=1, pady=15, padx=20)
        self.recipient_last_name_e.grid(column=1, row=2, pady=5)
        self.recipient_last_name_l.grid(column=0, row=2, sticky=W)
        self.recipient_first_name_e.grid(column=1, row=1)
        self.recipient_first_name_l.grid(column=0, row=1, sticky=W)
        self.grid(column=0, row=0, pady=15, padx=15)

    def complete_email(self):
        recipient_email = self.recipient_email_e.get()
        if "@" in recipient_email:
            messagebox.showinfo(title="Attention",
                                message=f"recipient {recipient_email} include @ to apply auto fill remove it please.")
        elif recipient_email == "":
            messagebox.showinfo(title="Attention",
                                message="please don't leave it empty.")

        else:
            self.email_provider = self.var.get()
            self.recipient_email_e.delete(0, END)
            self.recipient_email_e.insert(0, recipient_email + self.email_provider)

    def save_recipient_email(self):
        new_data = {
            self.recipient_email_e.get(): {
                "first name": self.recipient_first_name_e.get().title(),
                "last name": self.recipient_last_name_e.get().title(),
            }
        }
        if len(self.recipient_email_e.get()) == 0 and len(self.recipient_first_name_e.get()) == 0 and len(
                self.recipient_last_name_e.get()) == 0:
            messagebox.showinfo(title="Attention",
                                message="please don't leave email and recipient first , last name empty")
        else:
            if os.path.isfile("data/recipient_data.json"):
                with open("data/recipient_data.json") as data_file:
                    data = json.load(data_file)
                    if self.recipient_email_e.get() in data:
                        messagebox.showinfo(title="Attention",
                                            message=f"recipient {self.recipient_email_e.get()} is already existed.")
                        self.clear_all_entries()
                    else:
                        with open("data/recipient_data.json", "r") as data_file:
                            data = json.load(data_file)
                            data.update(new_data)
                        with open("data/recipient_data.json", "w") as data_file:
                            json.dump(data, data_file, indent=4)
                        messagebox.showinfo(title="Attention",
                                            message=f"recipient {self.recipient_email_e.get()} added successfully.")
                        self.pick_recipient_email_list.insert(END, self.recipient_email_e.get())
                        self.clear_all_entries()

            else:
                with open("data/recipient_data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
                messagebox.showinfo(title="Attention",
                                    message=f"recipient {self.recipient_email_e.get()} added successfully.")
                self.pick_recipient_email_list.insert(END, self.recipient_email_e.get())
                self.clear_all_entries()

    def clear_all_entries(self):
        self.recipient_first_name_e.delete(0, END)
        self.recipient_last_name_e.delete(0, END)
        self.recipient_email_e.delete(0, END)

    def update_list_box(self):
        if os.path.isfile("data/recipient_data.json"):
            with open("data/recipient_data.json", "r") as data_file:
                data = json.load(data_file)
            for email in data:
                self.pick_recipient_email_list.insert(END, email)

    def next_step(self):
        self.email_selected = self.pick_recipient_email_list.get(ANCHOR)
        if len(self.email_selected) > 0:
            pass
            # tm.SetupEmail(root=self.root, recipient_email=self.email_selected, password=self.password)
        else:
            messagebox.showinfo(title="Attention",
                                message=f"You did not select any email yet..")

    def delete_email(self):
        self.email_selected = self.pick_recipient_email_list.get(ANCHOR)
        with open("data/recipient_data.json", "r") as data_file:
            data = json.load(data_file)
            if self.email_selected in data:
                ask_y_n = messagebox.askyesno(title="Deletion Confirmation", message=f"Are you sure that you want to "
                                                                                     f"delete {self.email_selected}")
                if ask_y_n:
                    del data[self.email_selected]
                    data.update(data_file)
                    self.pick_recipient_email_list.delete(ANCHOR)
            else:
                messagebox.showinfo(title="Attention",
                                    message=f"You  did not select any recipient email yet..")

        with open("data/recipient_data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)
