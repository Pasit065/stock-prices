# Stock-Prices
**Stock-Prices** projects is developed by Python using REST API to provide and evaluate the stock prices of determined company between two days and notify users to SMS and email with the percentage of stock prices change and related news.

## Overview
The project utilize REST API to get stock prices of specific company and evealuate the percentage of stock prices changing between 2 days. 

The percentage is utilized as compared value. Additionally, the news and SMS is provided when the percentage is changed significantly more than 5 %. Afterward, email and SMS will be used as notification tools to sent notification to user.

## API 
The project developed and utilize 2 REST API.

1. **Alphavantage** used for provide stock prices data of specific company with determine specific interval. See more *[Alphavantage Website](https://www.alphavantage.co/)*

2. **News API** used for getting news topic and article data of specific company. See more *[News API](https://newsapi.org )*

## Diagram
### Flowchart

## Usage 
Before executing projects, a few initial setup is necessary.

### Initial Setup
1. Please make sure your *Python Version* is updated to lastest version, recommanded version is version that higher than `3.10.0`
    ```Bash
    python --version
    ```

2. Install all necessary packages.
    ```
    pip install -r requirements.txt
    ```

3. Log in `Twilio` account and get `auth_token` and `account_sid` to provide into `main.py` as environment variables.
    ```Python
    auth_token = os.environ.get("auth_token")
    account_sid = os.environ.get("account_sid")
    ```

    When `Twilio` account has been registered, user will get **Twilio phone number** determined it and user phone number into `main.py` as environment variables.
    ```Python
    twilio_phone_num = os.environ.get("twilio_phone_number") 
    recieved_sms_phone_num = os.environ.get("my_phone_number")
    ```

4. Register to **Alphavantage** and **News API** account to get *API keys* and determined it as environment variables in `main.py`.
    ```Python
    stock_api_key = os.environ.get("stock_api_key")
    news_api_key = os.environ.get("news_api_key")
    ```

5. Provided user *email* and *app password* to `main.py` as environment variables.
    ```Python
    my_email = os.environ.get("my_email")
    smtp_pass = os.environ.get("smtp_pass")
    ```

### Custom Setup 
1. `STOCK` and `COMPANY_NAME` are not fixed, which means users can change it to other company but `STOCK` and `COMPANY_NAME` must be the same company. If company has been changed `tesla.py` modules named must be changed for example.

    In `main.py`
    ```Python
    STOCK = "NVDA"
    COMPANY_NAME = "NVIDIA Corp"
    ```

    In `tesla.py` is changed to `nvidia.py` and internal class must be changed.
    ```Python
    import requests

    class Nvidia():
        ...
    ```

2. Percent threshold to compared can be changed in `main.py` as example below.
    ```Python
    if tesla.percentage_diff_price >= 3 or tesla.percentage_diff_price <= -2:
        ...
    ```

3. 
### Executing Project
If all necessary setup have been provided, project will be executed by below command.
```
python main.py
```