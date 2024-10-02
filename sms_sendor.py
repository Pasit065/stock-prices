from twilio.rest import Client
import os

class SmsSendor():
    # This class is responsible with execute SMS notify and managing SMS message. 
    def __init__(self, twilio_number, sms_recieved_phone_num):
        self.send_sms_message_list = []
        self.twilio_phone_num = twilio_number
        self.sms_recieved_phone_num = sms_recieved_phone_num

    def creating_sms_message_list(self, tesla, stock, percent_diff_text):
        for news in tesla.filtered_news_list:

            news_article = f"""
{stock}: {percent_diff_text}
Headline: {news["title"]}
description: {news["description"]}"""

            self.send_sms_message_list.append(news_article)

    def sending_sms(self, auth_token, account_sid):
        client = Client(account_sid, auth_token)
        sms_number = 1

        for sms_message in self.send_sms_message_list:
            message = client.messages.create(
                from_ = self.twilio_phone_num,
                body = sms_message,
                to = self.sms_recieved_phone_num)

            print(f"~~~message number {sms_number} sending successful~~~\nYou can check some news on you sms in your devices.")
            sms_number += 1
        
            
            


