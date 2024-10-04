from tesla import Tesla
from percent_diff_stock_calculator import PercentDiffStockCalculator
from sms_sendor import SmsSendor
from email_sendor import EmailSendor
import smtplib as smtp
import os
import requests

 # symbol value.
STOCK = "TSLA"             
COMPANY_NAME = "Tesla Inc"

def show_send_sms_news(sms_sendor):
    """Shows user's sms message that to will be send to their sms."""
    news_no = 0

    for message in sms_sendor.send_sms_message_list:
        news_no += 1
        print(f"{news_no}.): {message}\n")

# Determine every environment variables.
auth_token = os.environ.get("auth_token")
account_sid = os.environ.get("account_sid")

# Get all api keys of every api.
stock_api_key = os.environ.get("stock_api_key")
news_api_key = os.environ.get("news_api_key")

# Get twilio phone number and recieved sms phone number.
twilio_phone_num = os.environ.get("twilio_phone_number") 
recieved_sms_phone_num = os.environ.get("my_phone_number")

# Get my email and app password.
my_email = os.environ.get("my_email")
smtp_pass = os.environ.get("smtp_pass")

# smtp connection.
connection = smtp.SMTP("smtp.gmail.com", port = 587)
connection.starttls()
connection.login(user = my_email, password = smtp_pass)

# Determine every objects.
tesla = Tesla() 
percentage_diff_stock_calculator = PercentDiffStockCalculator()
sms_sendor = SmsSendor(twilio_number = twilio_phone_num, sms_recieved_phone_num = recieved_sms_phone_num)
email_sendor = EmailSendor(from_email = my_email, to_email = my_email)

# Determine stock price parameters for api gets.
stock_api_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": stock_api_key
}

# Getting tesla's stock price from api get. 
response = requests.get(url = 'https://www.alphavantage.co/query?', params = stock_api_params)
stock_data = response.json()

# Determine every data for calculating and considerd days.
tesla.set_initial_and_final_prices_for_considerd_days(stock_data = stock_data)

# Calculating percentage of difference price between days in lastest days.
tesla.percentage_diff_price = percentage_diff_stock_calculator.calculating_percents_pers_days(tesla = tesla)
tesla.percentage_diff_price = round(tesla.percentage_diff_price, 2)

# Print the result of calculation.
print(f"Differrence percent of stock price between lastest days is {tesla.percentage_diff_price}%\n")

# Check if percent increase or decrease by 5% then searching news and sending 3 sms messages to user's phone.
if tesla.percentage_diff_price >= 5 or tesla.percentage_diff_price <= -5:
    # Getting every tesla news from lastest days to current days.
    every_tesla_news = tesla.get_every_news_of_tesla(news_api_key = news_api_key)

    # Check if Tesla stock rise up or not.
    is_percent_diff_rise_up = percentage_diff_stock_calculator.is_percent_diff_rise_up(tesla = tesla)

    # Getting percent display text.
    if is_percent_diff_rise_up:
        percent_diff_text = f"🔺{tesla.percentage_diff_price}%"
        email_percent_text = f"Stock price rise up by {tesla.percentage_diff_price}%"
    elif not is_percent_diff_rise_up:
        percent_diff_text = f"🔻{tesla.percentage_diff_price}%"
        email_percent_text = f"Stock price decrease by {tesla.percentage_diff_price}%"

    # Filtering 3 news to given list.
    tesla.getting_filtered_news_list(every_tesla_news = every_tesla_news, the_amount_of_news = 3)

    # Creating sms messages from 3 sms articles.
    sms_sendor.creating_sms_message_list(tesla = tesla, stock = STOCK, percent_diff_text = percent_diff_text)

    # Sending 3 sms to user's phone.
    show_send_sms_news(sms_sendor = sms_sendor)

    try:
        sms_sendor.sending_sms(auth_token = auth_token, account_sid = account_sid)
    except: 
        # If error has occured while sending sms 'email_sendor' will send notification to user email.
        error_sms_body_message = """
Stock-Prices script can't send sms.

Please go to https://www.twilio.com/docs/errors/20003 to see more details.
"""

        email_msg = email_sendor.get_email_message(header = "Sms sending has been interupted.", message = error_sms_body_message)
        email_sendor.send_email(connection = connection, email_msg = email_msg)

        raise ValueError("""Can't send sms maybe it is caused by lack of authencate number that cause 
Unable to create record: Authenticate. Please go to https://www.twilio.com/docs/errors/20003 to see more details""")
    
    # If sms have been send successfully, 'email_sendor' will notify users.
    successfully_sms_body_message = f"""
Differrence percent of stock price between lastest days is {email_percent_text} and SMS {len(sms_sendor.send_sms_message_list)} have 
"""

    email_msg = email_sendor.get_email_message(header = "Sms message has been send successfully.", message = successfully_sms_body_message)
    email_sendor.send_email(connection = connection, email_msg = email_msg)

else:
    # If sms haven't been send, 'email_sendor' will notify users.
    unsend_sms_body_message = """
The message haven't been send due to percentage of stock price between days didn't 
reach to lower than -5% or higher than 5%.
"""

    email_msg = email_sendor.get_email_message(header = "Sms message haven't been send.", message = unsend_sms_body_message)
    email_sendor.send_email(connection = connection, email_msg = email_msg)