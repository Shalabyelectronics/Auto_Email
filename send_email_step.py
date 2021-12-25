import json
from tkinter import *
import random
from tkinter import messagebox, filedialog
import os
import smtplib
from email.message import EmailMessage
from tkcalendar import Calendar
import imghdr

FONT = "Baloo Bhaijaan 2"
BACKGROUND_COLOR = "#F6F2D4"
FOREGROUND_COLOR = "#22577E"
LINES = "#95D1CC"
BORDER = "#5584AC"


class SendEmail(Frame):
    def __init__(self, root, from_email, to_email):
        super().__init__()
        self.attachments_list_paths = None
        self.msg_subject = None
        self.temp_msg = None
        self.user_msg_template = None
        self.quote_picked = None
        self.recipient_full_name = None
        self.sender_smtp = None
        self.sender_password = None
        self.sender_full_name = None
        self.root = root
        self.from_email = from_email
        self.to_email = to_email
        self.config(bg=BACKGROUND_COLOR, bd=5, pady=5, padx=15)
        self.your_section_l = Label(self, text="We are going to schedule sending your email.",
                                    font=(FONT, 18, "bold"),
                                    fg=FOREGROUND_COLOR,
                                    bg=BACKGROUND_COLOR, relief="sunken", bd=3, padx=5, pady=5)
        self.from_l = Label(self, text="From E-mail : ", font=(FONT, 15), fg=FOREGROUND_COLOR,
                            bg=BACKGROUND_COLOR)
        self.from_e = Entry(self, font=(FONT, 15, "bold"), fg="white", width=20, bg=LINES)
        self.from_e.insert(0, self.from_email)

        self.to_l = Label(self, text="To E-mail : ", font=(FONT, 15), fg=FOREGROUND_COLOR,
                          bg=BACKGROUND_COLOR)
        self.to_e = Entry(self, font=(FONT, 15, "bold"), fg="white", width=20, bg=LINES)
        self.to_e.insert(0, self.to_email)
        self.message_field = Text(self, width=40, height=15, padx=5, pady=5, font=(FONT, 12, "bold"),
                                  fg=FOREGROUND_COLOR, bg=BACKGROUND_COLOR, relief="sunken", bd=9, wrap=WORD)
        self.send_now_button = Button(self, text="Send now", width=19, font=(FONT, 15, "bold"),
                                      fg=FOREGROUND_COLOR,
                                      bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR, highlightthickness=0,
                                      command=self.send_now)
        self.add_attachment_button = Button(self, text="Add attachment", width=15, font=(FONT, 15, "bold"),
                                            fg=FOREGROUND_COLOR,
                                            bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR,
                                            highlightthickness=0, command=self.add_attachment_to_listbox)
        self.delete_attachment_button = Button(self, text="Delete attachment", width=16, font=(FONT, 15, "bold"),
                                               fg=FOREGROUND_COLOR,
                                               bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR,
                                               highlightthickness=0, command=self.delete_attachment_from_listbox)
        self.send_later_button = Button(self, text="Send later", width=16, font=(FONT, 15, "bold"),
                                        fg=FOREGROUND_COLOR,
                                        bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR,
                                        highlightthickness=0, command=self.send_later)
        self.attachment_l = Label(self, text="Attachments.",
                                  font=(FONT, 15, "bold"),
                                  fg=FOREGROUND_COLOR,
                                  bg=BACKGROUND_COLOR, relief="sunken", bd=3)
        self.attachments_list = Listbox(self, width=50, height=15, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR,
                                        font=(FONT, 10, "bold"))
        self.templates_list = os.listdir("data/letter_templates")
        self.var = StringVar(self)
        self.var.set(self.templates_list[0])
        self.choose_template_l = Label(self, text="Choose template :",
                                       font=(FONT, 15, "bold"),
                                       fg=FOREGROUND_COLOR,
                                       bg=BACKGROUND_COLOR, relief="sunken", bd=3)
        self.templates_option = OptionMenu(self, self.var, *self.templates_list,
                                           command=self.create_message_from_template)
        self.templates_option.config(font=(FONT, 15, "bold"), fg=FOREGROUND_COLOR, bg=BACKGROUND_COLOR,
                                     activebackground=BACKGROUND_COLOR)
        self.template_menu = self.nametowidget(self.templates_option.menuname)
        self.template_menu.config(font=(FONT, 12, "bold"), fg=FOREGROUND_COLOR, bg=BACKGROUND_COLOR,
                                  activebackground=FOREGROUND_COLOR)
        self.msg_title = Label(self, text="Message title:",
                               font=(FONT, 15, "bold"),
                               fg=FOREGROUND_COLOR,
                               bg=BACKGROUND_COLOR, relief="sunken", bd=3)

        self.msg_title_e = Entry(self, font=(FONT, 15, "bold"), fg="white", width=20, bg=LINES)
        self.choose_template_l.grid(column=0, row=6)
        self.templates_option.grid(column=1, row=6)
        self.msg_title_e.grid(column=1, row=2, sticky=W)
        self.msg_title.grid(column=0, row=2, sticky=W)
        self.attachment_l.grid(column=2, row=2, columnspan=2)
        self.attachments_list.grid(column=2, row=3, columnspan=2, rowspan=3, pady=15, padx=15)
        self.add_attachment_button.grid(column=2, row=6, pady=15)
        self.send_later_button.grid(column=2, row=7, columnspan=2, pady=15)
        self.delete_attachment_button.grid(column=3, row=6, pady=15)
        self.send_now_button.grid(column=0, row=7, columnspan=2, pady=15)
        self.message_field.grid(column=0, row=3, columnspan=2, rowspan=3, pady=15)
        self.to_e.grid(column=3, row=1, pady=15, sticky=W)
        self.to_l.grid(column=2, row=1, sticky=E, padx=15)
        self.from_e.grid(column=1, row=1, pady=15, sticky=W)
        self.from_l.grid(column=0, row=1, sticky=W)
        self.your_section_l.grid(column=0, row=0, columnspan=4)
        self.grid(column=0, row=0, pady=15, padx=15)

    def sender_data(self):
        with open("data/your_data.json", "rt") as sender_data_file:
            sender_data = json.load(sender_data_file)
            if self.from_email in sender_data:
                self.sender_full_name = sender_data[self.from_email]["first name"] + " " + sender_data[self.from_email][
                    "last name"]
                self.sender_password = sender_data[self.from_email]["password"]
                self.sender_smtp = sender_data[self.from_email]["smtp"]

    def recipient_data(self):
        with open("data/recipient_data.json", "rt") as recipient_data_file:
            recipient_data = json.load(recipient_data_file)
            if self.to_email in recipient_data:
                self.recipient_full_name = recipient_data[self.to_email]["first name"] + " " + \
                                           recipient_data[self.to_email]["last name"]

    def pick_random_quote(self):
        with open("data/quotes.txt", "rt") as quotes_data_file:
            quotes_data = quotes_data_file.readlines()
            random_quote_index = random.randint(0, len(quotes_data))
            self.quote_picked = quotes_data[random_quote_index]

    def create_message_from_template(self, *args):
        self.message_field.delete("1.0", "end")
        self.recipient_data()
        self.sender_data()
        self.pick_random_quote()
        replacement_words = {
            "[RECIPIENT_NAME]": self.recipient_full_name,
            "[QUOTES]": self.quote_picked,
            "[SENDER_NAME]": self.sender_full_name
        }
        self.user_msg_template = self.var.get()
        if self.user_msg_template in self.templates_list:
            with open(f"data/letter_templates/{self.user_msg_template}", "rt") as msg_template_file:
                msg_template_data = msg_template_file.read()
                for old_word, new_word in replacement_words.items():
                    if old_word in msg_template_data:
                        msg_template_data = msg_template_data.replace(old_word, new_word)

            with open("data/letter_templates/temp_letter.txt", "wt") as temp_letter_file:
                new_letter = temp_letter_file.write(msg_template_data)

            with open("data/letter_templates/temp_letter.txt", "rt") as temp_letter_file:
                new_letter = temp_letter_file.read()
                self.message_field.insert(INSERT, new_letter)

    def send_now(self):
        if len(self.to_e.get()) != 0 and len(self.from_e.get()) != 0 and len(
                self.message_field.get("1.0", "end")) != 1 and len(self.msg_title_e.get()) != 0:
            self.sender_data()
            self.recipient_data()
            self.temp_msg = self.message_field.get("1.0", "end")
            self.msg_subject = self.msg_title_e.get()
            msg = EmailMessage()
            msg["Subject"] = self.msg_subject
            msg["From"] = self.from_email
            msg["To"] = self.to_email
            msg.set_content(self.temp_msg)
            if len(self.attachments_list_paths) != 0:
                for file in self.attachments_list_paths:
                    try:
                        with open(file, "rb") as f:
                            file_data = f.read()
                            file_type = imghdr.what(f.name)
                            file_name = os.path.basename(file)
                        msg.add_attachment(file_data, maintype="image", subtype=file_type, filename=file_name)
                    except:
                        with open(file, "rb") as f:
                            file_data = f.read()
                            file_name = os.path.basename(file)
                        msg.add_attachment(file_data, maintype="application", subtype="octet-stream",
                                           filename=file_name)

            with smtplib.SMTP_SSL(self.sender_smtp, port=465) as connection:
                connection.login(self.from_email, self.sender_password)
                connection.send_message(msg)
                messagebox.showinfo(title="Attention",
                                    message=f"your message sent successfully to {self.to_email}")
        else:
            messagebox.showinfo(title="Attention",
                                message=f"Please, don't leave any of the necessary fields empty.")

    def add_attachment_to_listbox(self):
        self.attachments_list_paths = list(filedialog.askopenfilenames(initialdir="/", title="Select files to attach",
                                                                       filetypes=(
                                                                           ("jpeg files", "*.jpg"),
                                                                           ("all files", "*.*"))))
        for attach in range(len(self.attachments_list_paths)):
            self.attachments_list.insert(attach, self.attachments_list_paths[attach])

    def delete_attachment_from_listbox(self):
        if self.attachments_list.get(ANCHOR) in self.attachments_list_paths:
            self.attachments_list_paths.pop(self.attachments_list_paths.index(self.attachments_list.get(ANCHOR)))
            self.attachments_list.delete(ANCHOR)
        else:
            self.attachments_list.delete(ANCHOR)

    def send_later(self):
        # current_folder = os.getcwd()
        # recipient_attachment_folder = os.mkdir(f"{current_folder}/recipient_email_date")
        pick_date_time_window = Toplevel()
        pick_date_time_window.geometry("+700+150")
        pick_date_time_window.config(bg=FOREGROUND_COLOR, padx=15, pady=15, relief="sunken", bd=10)
        pick_date_time_window.title("Pick date and time")
        pick_date_time_window.iconbitmap("img/my.ico")
        title_label = Label(pick_date_time_window, text="Pick date and time",
                            font=(FONT, 15, "bold"), fg=BACKGROUND_COLOR,
                            bg=FOREGROUND_COLOR)
        calendar = Calendar(pick_date_time_window, selectmode="day", year=2021, month=12, day=30)
        time_title_label = Label(pick_date_time_window, text="Hours  :  minutes  : seconds", font=(FONT, 15, "bold"),
                                 fg=BACKGROUND_COLOR,
                                 bg=FOREGROUND_COLOR)
        hour_string = StringVar()
        minute_string = StringVar()
        second_string = StringVar()
        hour_sb = Spinbox(pick_date_time_window, from_=0, to=23, wrap=True, textvariable=hour_string, width=2,
                          state="readonly",
                          font=("Times", 20), justify=CENTER, fg=FOREGROUND_COLOR)
        minute_sb = Spinbox(pick_date_time_window, from_=0, to=59, wrap=True, textvariable=minute_string, width=2,
                            state="readonly",
                            font=("Times", 20), justify=CENTER, fg=FOREGROUND_COLOR)
        second_sb = Spinbox(pick_date_time_window, from_=0, to=59, wrap=True, textvariable=second_string, width=2,
                            state="readonly",
                            font=("Times", 20), justify=CENTER, fg=FOREGROUND_COLOR)
        save_datetime_b = Button(pick_date_time_window, text="Save", font=(FONT, 15, "bold"), fg=FOREGROUND_COLOR,
                                 bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR, highlightthickness=0)

        title_label.pack(side=TOP)
        calendar.pack(side=TOP)
        time_title_label.pack(side=TOP)
        save_datetime_b.pack(side=BOTTOM, pady=20)
        hour_sb.pack(side=LEFT, fill=X, expand=True)
        minute_sb.pack(side=LEFT, fill=X, expand=True)
        second_sb.pack(side=LEFT, fill=X, expand=True)
