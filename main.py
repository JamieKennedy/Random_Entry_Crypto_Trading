import configparser
from Account import Account
import time
import random


def main():
    keys = get_keys("secret/config.txt")

    initial_currencies = init_currencies(["BTC"])
    account = Account(keys, 0, initial_currencies)
    account.deposit_currency("BTC", 0.0038)
    account.deposit_balance(100)

    account.update_account_value()
    account.starting_value = account.account_value

    account.print_account_summary()

    t = time.time()
    open_position(account, "BTC")

    account.print_account_summary()

    while time.time() - t < 600:
        positions = account.check_positions()

        for position in positions:
            account.close_position(position)
            open_position(account, "BTC")

        account.print_account_summary()

        time.sleep(5)

    account.close_all_positions()
    account.print_account_summary()


def open_position(account, currency):
    actions = ["buy", "sell"]

    action = random.choice(actions)
    if action == "buy":
        account.open_position(action, currency, account.balance * 0.5, None)
    else:
        account.open_position(action, currency, None, account.currencies[currency] * 0.5)


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