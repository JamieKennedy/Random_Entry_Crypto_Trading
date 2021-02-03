import time


class Position:
    def __init__(self, action, currency, open_value, currency_amount, client):
        self.open_time = time.time()
        self.action = action
        self.currency = currency
        self.open_value = open_value
        self.current_value = open_value
        self.result = 0
        self.currency_amount = currency_amount
        self.client = client
        self.price = self.get_current_price()

        if action == "buy":
            self.take_profit = float(open_value) * 1.001
            self.stop_loss = float(open_value) * 0.999
        else:
            self.take_profit = float(open_value) * 0.999
            self.stop_loss = float(open_value) * 1.001

    def update_position(self):
        self.current_value = self.get_current_value()
        self.price = self.get_current_price()
        self.result = self.get_current_result()

    def get_current_value(self):
        ticker = self.client.get_product_ticker(self.currency + "-GBP")

        return float(ticker["price"]) * self.currency_amount

    def get_current_price(self):
        ticker = self.client.get_product_ticker(self.currency + "-GBP")

        return float(ticker["price"])

    def get_current_result(self):
        if self.action == "buy":
            return self.current_value - self.open_value
        else:
            return self.open_value - self.current_value

    def get_position_data(self):
        self.update_position()

        open_time = "Open Time: {}\n".format(self.open_time)
        action = "Action: {}\n".format(self.action)
        currency = "Currency: {}\n".format(self.currency)
        open_value = "Open Value: £{:,.2f}\n".format(self.open_value)
        current_value = "Current Value: £{:,.2f}\n".format(self.current_value)
        result = "Result: £{:,.2f}\n".format(self.result)
        amount = "Amount: {}\n".format(self.currency_amount)
        price = "Price: £{:,.2f}\n".format(self.price)

        data = open_time + action + currency + open_value + current_value + result + amount + price

        return data

    def close_position(self):
        ticker = self.client.get_product_ticker(self.currency + "-GBP")
        self.update_position()

        return {
            "action": self.action,
            "currency": self.currency,
            "current_value": self.current_value,
            "currency_amount": self.currency_amount,
            "result": self.result
        }
