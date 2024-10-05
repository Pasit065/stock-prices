class PercentDiffStockCalculator():
    # This class is responsible with handling and analyse percent different between intraday.
    def calculating_percents_pers_days(self, tesla):
        return ((tesla.final_days_price - tesla.initial_days_price) / tesla.initial_days_price) * 100

    def is_percent_diff_rise_up(self, tesla):       
        if tesla.percentage_diff_price >= 0:
            return True
        elif tesla.percentage_diff_price < 0:
            return False