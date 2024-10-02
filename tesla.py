import requests

class Tesla():
    # This class is responsible with handling 'Tesla' data.  
    def __init__(self):
        self.final_days_price = None
        self.initial_days_price = None
        self.percentage_diff_price = None
        self.initial_days_of_news = None
        self.filtered_news_list = None

    def set_initial_and_final_prices_for_considerd_days(self, stock_data):

        total_days = 0

        for days in stock_data["Time Series (Daily)"]:

            total_days += 1

            if total_days == 1:
                self.initial_days_of_news = days
                self.final_days_price = float(stock_data["Time Series (Daily)"][days]["4. close"])
            elif total_days >= 2:
                self.initial_days_price = float(stock_data["Time Series (Daily)"][days]["4. close"])
                break

    def get_every_news_of_tesla(self, news_api_key):

        news_params = {
        "apiKey": news_api_key,
        "q": "Tesla Inc",
        "qInTitle": "Stock price",
        "from": self.initial_days_of_news,
        "language": "en"
        }
        
        response = requests.get(url = "https://newsapi.org/v2/everything?", params = news_params)

        return response.json()
    
    def getting_filtered_news_list(self, every_tesla_news, the_amount_of_news = 3):
        
        total_news = 0
        self.filtered_news_list = []

        for news in every_tesla_news["articles"]:
            self.filtered_news_list.append(news)
    
            total_news += 1

            if total_news >= the_amount_of_news:
                break 

        
