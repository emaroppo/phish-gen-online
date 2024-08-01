import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pymongo import MongoClient
from datetime import datetime


class EmailSender:
    def __init__(self, sender_email, sender_password):
        self.db = MongoClient("localhost", 27017)["online_fine_tuning"]
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.receiver_emails = list()
        self.server = smtplib.SMTP("localhost", 1025)
        # self.server.starttls()
        # self.server.login(self.sender_email, self.sender_password)

    def send_email(self):
        # pick random email from database
        message = self.db["outgoing"].find_one()
        receiver_email = random.choice(self.receiver_emails)

        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = receiver_email
        msg["Subject"] = message["prompt"]["subject"]
        msg.attach(MIMEText(message["body"], "plain"))
        text = msg.as_string()
        self.server.sendmail(self.sender_email, receiver_email, text)

        # move message from outgoing to sent adding sent_at field
        message["sent_at"] = datetime.now()
        self.db["sent_emails"].insert_one(message)
        self.db["outgoing"].delete_one({"_id": message["_id"]})


# send a test email
sender = EmailSender("hello@local.com", "pw")
sender.receiver_emails = ["goodbye@local.com"]
sender.send_email()
