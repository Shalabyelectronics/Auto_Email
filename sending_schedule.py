import json
import os.path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

FONT = "Baloo Bhaijaan 2"
BACKGROUND_COLOR = "#F6F2D4"
FOREGROUND_COLOR = "#22577E"
LINES = "#95D1CC"
BORDER = "#5584AC"


class SendingScheduleManager(Toplevel):
    def __init__(self, root):
        super().__init__()
        self.id_selected = None
        self.config(bg=BACKGROUND_COLOR)
        self.title("Sending Schedule Manager")
        self.iconbitmap("img/my.ico")
        self.geometry("+500+50")
        self.show_data_frame = LabelFrame(self, text="Sending schedule", font=(FONT, 15, "bold"), fg=FOREGROUND_COLOR,
                                          bg=BACKGROUND_COLOR)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Treeview",
                             background=BACKGROUND_COLOR,
                             foreground=FOREGROUND_COLOR,
                             font=(FONT, 12, "bold"),
                             rowheight=25,
                             fieldbackground=BACKGROUND_COLOR)
        self.style.configure("Treeview.Heading", background=FOREGROUND_COLOR,
                             foreground=BACKGROUND_COLOR,
                             font=(FONT, 13, "bold"),
                             rowheight=50,
                             fieldbackground=BACKGROUND_COLOR)
        self.style.map("Treeview.Heading", background=[("selected", FOREGROUND_COLOR)])
        self.style.map("Treeview", background=[("selected", FOREGROUND_COLOR)])
        self.show_treeview = ttk.Treeview(self.show_data_frame,
                                          columns=("recipient_id", "from_email", "to_email",
                                                   "attachment", "date", "time"), show="headings", height=6, padding=15,
                                          selectmode="browse")
        self.show_treeview.column("recipient_id", anchor=CENTER, width=25)
        self.show_treeview.column("from_email", anchor=W, width=200)
        self.show_treeview.column("to_email", anchor=W, width=200)
        self.show_treeview.column("attachment", anchor=CENTER, width=110)
        self.show_treeview.column("date", anchor=CENTER, width=120)
        self.show_treeview.column("time", anchor=CENTER, width=120)
        self.show_treeview.heading("recipient_id", text="ID", anchor=W)
        self.show_treeview.heading("from_email", text="From Email", anchor=CENTER)
        self.show_treeview.heading("to_email", text="To Email", anchor=CENTER)
        self.show_treeview.heading("attachment", text="Attachments")
        self.show_treeview.heading("date", text="Sending date", anchor=W)
        self.show_treeview.heading("time", text="Sending time", anchor=W)
        self.show_treeview.grid(column=0, row=0, columnspan=2, pady=10, padx=10)
        self.get_data_selected = Button(self.show_data_frame, text="Get more Details", width=19,
                                        font=(FONT, 15, "bold"),
                                        fg=FOREGROUND_COLOR,
                                        bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR, highlightthickness=0,
                                        command=self.get_more_details)
        self.delete_selected_entry = Button(self.show_data_frame, text="Delete Selected", width=19,
                                            font=(FONT, 15, "bold"),
                                            fg=FOREGROUND_COLOR,
                                            bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR,
                                            highlightthickness=0,
                                            command=self.delete_from_data)
        self.delete_selected_entry.grid(column=1, row=1, pady=15)
        self.get_data_selected.grid(column=0, row=1, pady=15)
        self.show_data_frame.grid(column=0, row=0, pady=10, padx=10)
        self.show_details_frame = LabelFrame(self, text="Email Details", font=(FONT, 15, "bold"),
                                             fg=FOREGROUND_COLOR,
                                             bg=BACKGROUND_COLOR)
        self.subject_msg_l = Label(self.show_details_frame, text="Message Subject : ", font=(FONT, 15),
                                   fg=FOREGROUND_COLOR,
                                   bg=BACKGROUND_COLOR)
        self.subject_msg_l.grid(column=0, row=0, pady=15, padx=10)
        self.subject_msg_e = Entry(self.show_details_frame, font=(FONT, 15, "bold"), fg="white", width=20, bg=LINES)
        self.subject_msg_e.grid(column=1, row=0, pady=15, padx=10, sticky=W)
        self.content_msg_l = Label(self.show_details_frame, text="Message content : ", font=(FONT, 15),
                                   fg=FOREGROUND_COLOR,
                                   bg=BACKGROUND_COLOR)
        self.content_msg_l.grid(column=0, row=1, pady=15, padx=10)
        self.content_msg_field = Text(self.show_details_frame, width=40, height=10, padx=5, pady=5,
                                      font=(FONT, 12, "bold"),
                                      fg=FOREGROUND_COLOR, bg=BACKGROUND_COLOR, relief="sunken", bd=9, wrap=WORD)
        self.content_msg_field.grid(column=1, row=1, pady=15, padx=10)
        self.attachment_l = Label(self.show_details_frame, text="Attachments", font=(FONT, 15),
                                  fg=FOREGROUND_COLOR,
                                  bg=BACKGROUND_COLOR)
        self.attachment_l.grid(column=2, row=0)
        self.attachments_list = Listbox(self.show_details_frame, width=20, height=10, bg=BACKGROUND_COLOR,
                                        fg=FOREGROUND_COLOR,
                                        font=(FONT, 10, "bold"))
        self.attachments_list.grid(column=2, row=1, padx=10)
        self.show_details_frame.grid(column=0, row=1, pady=10, padx=10, sticky=W)
        self.load_data_to_show_treeview()

    def load_data_to_show_treeview(self):
        with open("send_later/data/send_later_data.json", "r") as send_later_data_file:
            data = json.load(send_later_data_file)

            for i in data:
                if len(data[i]["attachment"]) > 0:
                    with_attachment = "Yes"
                else:
                    with_attachment = "No"
                self.show_treeview.insert(parent="", index="end", iid=i,
                                          values=(i, data[i]["from_email"], data[i]["to_email"],
                                                  with_attachment,
                                                  f"{data[i]['day']}/{data[i]['month']}/{data[i]['year']}",
                                                  f"{data[i]['hour']}: {data[i]['minute']}: {data[i]['second']}"))

    def get_more_details(self):
        self.wm_attributes("-topmost", False)
        try:
            self.id_selected = self.show_treeview.selection()[0]
        except IndexError:
            attention = messagebox.showinfo(title="attention", message="Please select any row from the table first.")
            if attention == "ok":
                self.wm_attributes("-topmost", True)
        else:
            with open("send_later/data/send_later_data.json", "r") as send_later_data_file:
                data = json.load(send_later_data_file)
                if self.id_selected in data:
                    subject = data[self.id_selected]["subject"]
                    message = data[self.id_selected]["message"]
                    attachment = data[self.id_selected]["attachment"]
                    self.subject_msg_e.delete(0, END)
                    self.attachments_list.delete(0, END)
                    self.subject_msg_e.insert(0, subject)
                    self.content_msg_field.delete("1.0", "end")
                    self.content_msg_field.insert(INSERT, message)
                    if len(attachment) > 0:
                        for file in range(len(attachment)):
                            self.attachments_list.insert(file, os.path.basename(attachment[file]))

    def delete_from_data(self):
        self.wm_attributes("-topmost", False)
        try:
            self.id_selected = self.show_treeview.selection()[0]
        except IndexError:
            attention = messagebox.showinfo(title="attention",
                                            message="Please select any row from the table first.")
            if attention == "ok":
                self.wm_attributes("-topmost", True)

        else:
            confirmation = messagebox.askyesno(title="Deletion Confirmation", message="Are you sure that you want to "
                                                                                      "delete this entry?")
            if confirmation:
                self.wm_attributes("-topmost", True)
                with open("send_later/data/send_later_data.json", "r") as send_later_data_file:
                    data = json.load(send_later_data_file)
                    del data[self.id_selected]
                    data.update(data)
                with open("send_later/data/send_later_data.json", "w") as send_later_data_file:
                    json.dump(data, send_later_data_file, indent=4)

                self.show_treeview.delete(self.id_selected)
                self.subject_msg_e.delete(0, END)
                self.content_msg_field.delete("1.0", "end")
                self.attachments_list.delete(0, END)
