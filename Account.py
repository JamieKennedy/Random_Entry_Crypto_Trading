import cbpro as cbp


class Account:
    positions = {}

    def __init__(self, keys, balance=0, currencies=None):
        self.client = cbp.AuthenticatedClient(keys["API_KEY"], keys["SECRET"], keys["PHRASE"])

        self.balance = balance

        if currencies is None:
            self.currencies = {}
        else:
            self.currencies = currencies

    def deposit_currency(self, currency, value):
        if currency in self.currencies:
            self.currencies[currency] += value
        else:
            self.currencies[currency] = value

    def deposit_balance(self, value):
        self.balance += value

    def print_account_summary(self):
        print("Balance: £{:,.2f}".format(self.balance))

        for currency in self.currencies:
            print("{}: {}".format(currency, self.currencies[currency]))

    def get_ticker(self, ticker):
        return self.client.get_product_ticker(ticker)

