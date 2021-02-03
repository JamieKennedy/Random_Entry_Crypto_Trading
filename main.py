import configparser
from Account import Account


def main():
    keys = get_keys("secret/config.txt")

    initial_currencies = init_currencies(["BTC", "ETH"])
    account = Account(keys, 0, initial_currencies)

    print(account.get_ticker("BTC-GBP"))


def init_currencies(starting_currencies):
    currencies = {}

    for currency in starting_currencies:
        currencies[currency] = 0

    return currencies


def get_keys(config_file):
    cfg = configparser.ConfigParser()
    cfg.read(config_file)

    keys = {
        "API_KEY": cfg.get("API Keys", "API_KEY"),
        "SECRET": cfg.get("API Keys", "API_SECRET"),
        "PHRASE": cfg.get("API Keys", "API_PHRASE")
    }

    return keys


if __name__ == "__main__":
    main()