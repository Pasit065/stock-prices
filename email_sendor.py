class EmailSendor():
    def __init__(self, from_email, to_email):
        self.from_email =  from_email
        self.to_email = to_email

    def get_email_message(self, header, message):
       return f"Subject: {header}\n" + message

    def send_email(self, connection, email_msg):
        connection.sendmail(
            from_addr = self.from_email,
            to_addrs = self.to_email,
            msg = email_msg
        )