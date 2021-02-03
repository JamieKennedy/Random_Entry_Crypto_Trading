import cbpro as cbp
import random
import time
from Position import Position


class Account:
    positions = {}

    def __init__(self, keys, balance=0, currencies=None):
        self.client = cbp.AuthenticatedClient(keys["API_KEY"], keys["SECRET"], keys["PHRASE"])

        self.balance = balance

        if currencies is None:
            self.currencies = {}
        else:
            self.currencies = currencies

        self.starting_value = self.get_account_value()
        self.account_value = self.starting_value

    def deposit_currency(self, currency, value):
        if currency in self.currencies:
            self.currencies[currency] += value
        else:
            self.currencies[currency] = value

    def deposit_balance(self, value):
        self.balance += value

    def print_account_summary(self):
        self.update_account_value()
        print("Balance: £{:,.2f}".format(self.balance))

        for currency in self.currencies:
            print("{}: {}".format(currency, self.currencies[currency]))

        print("Account Value: £{:,.2f}".format(self.account_value))
        print("Account Result: £{:,.2f}".format(self.account_value - self.starting_value))
        print("----------------")

    def get_account_value(self):
        total = self.balance

        for currency in self.currencies:
            ticker = self.client.get_product_ticker(currency + "-GBP")

            total += float(ticker["price"]) * self.currencies[currency]

        return total

    def update_account_value(self):
        self.account_value = self.get_account_value()

    def get_ticker(self, ticker):
        return self.client.get_product_ticker(ticker)

    def open_position(self, action, currency, open_value, currency_amount):
        position_id = self.get_id()

        # Check if position can be created
        if action == "buy":
            if open_value > self.balance:
                print("buy value exceeds balance")
            else:
                currency_amount = self.get_currency_amount_from_value(currency, open_value)
                self.positions[position_id] = Position(action, currency, open_value, currency_amount, self.client)
                self.balance -= open_value
                self.currencies[currency] += currency_amount
        if action == "sell":
            if currency_amount > self.currencies[currency]:
                print("sell value exceed {} balance".format(currency))
            else:
                open_value = self.get_value_from_currency_amount(currency, currency_amount)
                self.positions[position_id] = Position(action, currency, open_value, currency_amount, self.client)
                self.currencies[currency] -= currency_amount
                self.balance += open_value

        print("opened position")
        print(self.positions[position_id].get_position_data())
        print("----------------")

    def get_id(self):
        position_id = random.randint(1000000, 9999999)

        while id in self.positions:
            position_id = random.randint(1000000, 9999999)

        return position_id

    def get_currency_amount_from_value(self, currency, value):
        ticker = self.client.get_product_ticker(currency + "-GBP")

        return value / float(ticker["price"])

    def get_value_from_currency_amount(self, currency, amount):
        ticker = self.client.get_product_ticker(currency + "-GBP")

        return float(ticker["price"]) * amount

    def update_positions(self):
        for position_id in self.positions:
            self.positions[position_id].update_position()

    def print_positions(self):
        for position_id in self.positions:
            print("ID: {} \n{}".format(position_id, self.positions[position_id].get_position_data()))

    def close_position(self, position_id):
        result = self.positions[position_id].close_position()

        if result["action"] == "buy":
            self.currencies[result["currency"]] -= result["currency_amount"]
            self.balance += result["current_value"]
            print("Position closed")
        else:
            self.currencies[result["currency"]] += result["currency_amount"]
            self.balance -= result["current_value"]

        print("Position closed")
        print(self.positions[position_id].get_position_data())

        self.positions.pop(position_id)
        print("----------------")

    def check_positions(self):
        positions_to_be_closed = []
        self.update_positions()

        for position_id in self.positions:
            t = time.time()
            if t - self.positions[position_id].open_time > 60:
                positions_to_be_closed.append(position_id)

        return positions_to_be_closed

    def close_all_positions(self):
        for position_id in list(self.positions):
            self.close_position(position_id)
