import json
from tkinter import *
import random
from tkinter import messagebox
import os
import smtplib
from email.message import EmailMessage

FONT = "Baloo Bhaijaan 2"
BACKGROUND_COLOR = "#F6F2D4"
FOREGROUND_COLOR = "#22577E"
LINES = "#95D1CC"
BORDER = "#5584AC"


class SendEmail(Frame):
    def __init__(self, root, from_email, to_email):
        super().__init__()
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
        self.your_section_l = Label(self, text="we are going to\n schedule sending your email.",
                                    font=(FONT, 18, "bold"),
                                    fg=FOREGROUND_COLOR,
                                    bg=BACKGROUND_COLOR, relief="sunken", bd=5)
        self.from_l = Label(self, text="From E-mail : ", font=(FONT, 15), fg=FOREGROUND_COLOR,
                            bg=BACKGROUND_COLOR)
        self.from_e = Entry(self, font=(FONT, 15, "bold"), fg="white", width=20, bg=LINES)
        self.from_e.insert(0, self.from_email)

        self.to_l = Label(self, text="To E-mail : ", font=(FONT, 15), fg=FOREGROUND_COLOR,
                          bg=BACKGROUND_COLOR)
        self.to_e = Entry(self, font=(FONT, 15, "bold"), fg="white", width=20, bg=LINES)
        self.to_e.insert(0, self.to_email)
        self.message_field = Text(self, width=40, height=15, padx=5, pady=5, font=(FONT, 12,"bold"),
                                  fg=FOREGROUND_COLOR, bg=BACKGROUND_COLOR, relief="sunken", bd=9, wrap=WORD)
        self.generate_button = Button(self, text="Generate a message", width=19, font=(FONT, 15, "bold"),
                                      fg=FOREGROUND_COLOR,
                                      bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR, highlightthickness=0,
                                      command=self.pick_random_quote)
        self.attachment_button = Button(self, text="Add attachment", width=15, font=(FONT, 15, "bold"),
                                        fg=FOREGROUND_COLOR,
                                        bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR, highlightthickness=0)
        self.delete_attachment_button = Button(self, text="Delete attachment", width=16, font=(FONT, 15, "bold"),
                                               fg=FOREGROUND_COLOR,
                                               bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR,
                                               highlightthickness=0)
        self.next_button = Button(self, text="Final step", width=16, font=(FONT, 15, "bold"),
                                  fg=FOREGROUND_COLOR,
                                  bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR,
                                  highlightthickness=0)
        self.attachment_l = Label(self, text="Attachments showing here.",
                                  font=(FONT, 18, "bold"),
                                  fg=FOREGROUND_COLOR,
                                  bg=BACKGROUND_COLOR, relief="sunken", bd=5)
        self.attachments_list = Listbox(self, width=30, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR,
                                        font=(FONT, 15, "bold"))
        self.var = Variable()
        self.choose_msg_template_one = Radiobutton(self, text="Template one", variable=self.var, value="letter_1.txt",
                                                   bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR,
                                                   activebackground=BACKGROUND_COLOR, font=(FONT, 15),
                                                   command=self.create_message_from_template)
        self.choose_msg_template_two = Radiobutton(self, text="Template two", variable=self.var, value="letter_2.txt",
                                                   bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR,
                                                   activebackground=BACKGROUND_COLOR, font=(FONT, 15),
                                                   command=self.create_message_from_template)
        self.choose_msg_template_three = Radiobutton(self, text="Template three", variable=self.var,
                                                     value="letter_3.txt",
                                                     bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR,
                                                     activebackground=BACKGROUND_COLOR, font=(FONT, 15),
                                                     command=self.create_message_from_template)

        self.choose_msg_template_one.grid(column=0, row=4, pady=15)
        self.choose_msg_template_two.grid(column=1, row=4, pady=15)
        self.choose_msg_template_three.grid(column=2, row=4, pady=15)
        self.attachment_l.grid(column=2, row=0, columnspan=2, pady=15)
        self.attachments_list.grid(column=2, row=3, columnspan=2, pady=15, padx=15)
        self.attachment_button.grid(column=0, row=6, pady=15)
        self.next_button.grid(column=3, row=6, pady=15)
        self.delete_attachment_button.grid(column=2, row=6, pady=15)
        self.generate_button.grid(column=1, row=6, pady=15)
        self.message_field.grid(column=0, row=3, columnspan=2, pady=15)
        self.to_e.grid(column=3, row=1, pady=15)
        self.to_l.grid(column=2, row=1, sticky=W, padx=15)
        self.from_e.grid(column=1, row=1, pady=15, sticky=E)
        self.from_l.grid(column=0, row=1, sticky=W)
        self.your_section_l.grid(column=0, row=0, columnspan=2)
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

    def create_message_from_template(self):
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
        templates_list = os.listdir("data/letter_templates")
        if self.user_msg_template in templates_list:
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


"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" style="font-family:arial, 'helvetica neue', helvetica, sans-serif">
<head>
<meta charset="UTF-8">
<meta content="width=device-width, initial-scale=1" name="viewport">
<meta name="x-apple-disable-message-reformatting">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta content="telephone=no" name="format-detection">
<title>New message</title>
<!--[if (mso 16)]>
<style type="text/css">
a {text-decoration: none;}
</style>
<![endif]-->
<!--[if gte mso 9]><style>sup { font-size: 100% !important; }</style><![endif]-->
<!--[if gte mso 9]>
<xml>
<o:OfficeDocumentSettings>
<o:AllowPNG></o:AllowPNG>
<o:PixelsPerInch>96</o:PixelsPerInch>
</o:OfficeDocumentSettings>
</xml>
<![endif]-->
<!--[if !mso]><!-- -->
<link href="https://fonts.googleapis.com/css?family=Roboto:400,400i,700,700i" rel="stylesheet">
<!--<![endif]-->
<style type="text/css">
#outlook a {
padding:0;
}
.es-button {
mso-style-priority:100!important;
text-decoration:none!important;
}
a[x-apple-data-detectors] {
color:inherit!important;
text-decoration:none!important;
font-size:inherit!important;
font-family:inherit!important;
font-weight:inherit!important;
line-height:inherit!important;
}
.es-desk-hidden {
display:none;
float:left;
overflow:hidden;
width:0;
max-height:0;
line-height:0;
mso-hide:all;
}
[data-ogsb] .es-button {
border-width:0!important;
padding:10px 20px 10px 20px!important;
}
@media only screen and (max-width:600px) {p, ul li, ol li, a { line-height:150%!important } h1, h2, h3, h1 a, h2 a, h3 a { line-height:120% } h1 { font-size:30px!important; text-align:left } h2 { font-size:24px!important; text-align:left } h3 { font-size:20px!important; text-align:left } .es-header-body h1 a, .es-content-body h1 a, .es-footer-body h1 a { font-size:30px!important; text-align:left } .es-header-body h2 a, .es-content-body h2 a, .es-footer-body h2 a { font-size:24px!important; text-align:left } .es-header-body h3 a, .es-content-body h3 a, .es-footer-body h3 a { font-size:20px!important; text-align:left } .es-menu td a { font-size:14px!important } .es-header-body p, .es-header-body ul li, .es-header-body ol li, .es-header-body a { font-size:14px!important } .es-content-body p, .es-content-body ul li, .es-content-body ol li, .es-content-body a { font-size:14px!important } .es-footer-body p, .es-footer-body ul li, .es-footer-body ol li, .es-footer-body a { font-size:14px!important } .es-infoblock p, .es-infoblock ul li, .es-infoblock ol li, .es-infoblock a { font-size:12px!important } *[class="gmail-fix"] { display:none!important } .es-m-txt-c, .es-m-txt-c h1, .es-m-txt-c h2, .es-m-txt-c h3 { text-align:center!important } .es-m-txt-r, .es-m-txt-r h1, .es-m-txt-r h2, .es-m-txt-r h3 { text-align:right!important } .es-m-txt-l, .es-m-txt-l h1, .es-m-txt-l h2, .es-m-txt-l h3 { text-align:left!important } .es-m-txt-r img, .es-m-txt-c img, .es-m-txt-l img { display:inline!important } .es-button-border { display:inline-block!important } a.es-button, button.es-button { font-size:18px!important; display:inline-block!important } .es-adaptive table, .es-left, .es-right { width:100%!important } .es-content table, .es-header table, .es-footer table, .es-content, .es-footer, .es-header { width:100%!important; max-width:600px!important } .es-adapt-td { display:block!important; width:100%!important } .adapt-img { width:100%!important; height:auto!important } .es-m-p0 { padding:0px!important } .es-m-p0r { padding-right:0px!important } .es-m-p0l { padding-left:0px!important } .es-m-p0t { padding-top:0px!important } .es-m-p0b { padding-bottom:0!important } .es-m-p20b { padding-bottom:20px!important } .es-mobile-hidden, .es-hidden { display:none!important } tr.es-desk-hidden, td.es-desk-hidden, table.es-desk-hidden { width:auto!important; overflow:visible!important; float:none!important; max-height:inherit!important; line-height:inherit!important } tr.es-desk-hidden { display:table-row!important } table.es-desk-hidden { display:table!important } td.es-desk-menu-hidden { display:table-cell!important } .es-menu td { width:1%!important } table.es-table-not-adapt, .esd-block-html table { width:auto!important } table.es-social { display:inline-block!important } table.es-social td { display:inline-block!important } }
</style>
</head>
<body style="width:100%;font-family:arial, 'helvetica neue', helvetica, sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0">
<div class="es-wrapper-color" style="background-color:#F6F6F6">
<!--[if gte mso 9]>
<v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
<v:fill type="tile" color="#f6f6f6"></v:fill>
</v:background>
<![endif]-->
<table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-repeat:repeat;background-position:center top">
<tr>
<td valign="top" style="padding:0;Margin:0">
<table class="es-header" cellspacing="0" cellpadding="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
<tr>
<td align="center" style="padding:0;Margin:0">
<table class="es-header-body" cellspacing="0" cellpadding="0" bgcolor="#ffffff" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FFFFFF;width:600px">
<tr>
<td align="left" style="padding:0;Margin:0;padding-top:20px;padding-left:20px;padding-right:20px">
<table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
<tr>
<td align="center" valign="top" style="padding:0;Margin:0;width:560px">
<table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
<tr>
<td align="center" style="padding:0;Margin:0;font-size:0px"><img class="adapt-img" src="https://upjyrk.stripocdn.email/content/guids/cab_pub_7cbbc409ec990f19c78c75bd1e06f215/images/Present_Gift_Box_Pink_with_White_Bow_Christmas_New_Year.png" alt style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" width="210"></td>
</tr>
</table></td>
</tr>
</table></td>
</tr>
</table></td>
</tr>
</table>
<table class="es-content" cellspacing="0" cellpadding="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
<tr>
<td align="center" style="padding:0;Margin:0">
<table class="es-content-body" cellspacing="0" cellpadding="0" bgcolor="#ffffff" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FFFFFF;width:600px">
<tr>
<td align="left" style="padding:0;Margin:0;padding-top:20px;padding-left:20px;padding-right:20px">
<table width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
<tr>
<td valign="top" align="center" style="padding:0;Margin:0;width:560px">
<table width="100%" cellspacing="0" cellpadding="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
<tr>
<td align="center" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:roboto, 'helvetica neue', helvetica, arial, sans-serif;line-height:33px;color:#008080;font-size:22px"><strong>"Here add your Message"</strong></p></td>
</tr>
<tr>
<td align="center" style="padding:0;Margin:0"><h2 style="Margin:0;line-height:23px;mso-line-height-rule:exactly;font-family:arial, 'helvetica neue', helvetica, sans-serif;font-size:19px;font-style:normal;font-weight:normal;color:#800080"><strong>"Here add your Message"😍</strong></h2></td>
</tr>
</table></td>
</tr>
</table></td>
</tr>
</table></td>
</tr>
</table>
<table class="es-footer" cellspacing="0" cellpadding="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
<tr>
<td align="center" style="padding:0;Margin:0">
<table class="es-footer-body" cellspacing="0" cellpadding="0" bgcolor="#ffffff" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FFFFFF;width:600px">
<tr>
<td align="left" style="padding:0;Margin:0;padding-top:20px;padding-left:20px;padding-right:20px">
<table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
<tr>
<td align="center" valign="top" style="padding:0;Margin:0;width:560px">
<table cellpadding="0" cellspacing="0" width="100%" background="https://upjyrk.stripocdn.email/content/guids/cab_pub_7cbbc409ec990f19c78c75bd1e06f215/images/Red_Autumn_Leaves_Transparent_Clip_Art_Image.png" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-image:url(https://upjyrk.stripocdn.email/content/guids/cab_pub_7cbbc409ec990f19c78c75bd1e06f215/images/Red_Autumn_Leaves_Transparent_Clip_Art_Image.png);background-repeat:no-repeat;background-position:left top" role="presentation">
<tr>
<td align="center" style="padding:0;Margin:0;font-size:0px"><img class="adapt-img" src="https://upjyrk.stripocdn.email/content/guids/cab_pub_7cbbc409ec990f19c78c75bd1e06f215/images/59401543503928750.png" alt style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" width="560"></td>
</tr>
</table></td>
</tr>
</table></td>
</tr>
</table></td>
</tr>
</table></td>
</tr>
</table>
</div>
</body>
</html>
"""
