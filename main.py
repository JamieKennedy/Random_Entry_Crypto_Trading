import configparser
from Account import Account
import time
import random
import matplotlib.pyplot as plt


def main():
    keys = get_keys("secret/config.txt")

    initial_currencies = init_currencies(["BTC"])
    account = Account(keys, 0, initial_currencies)
    account.deposit_currency("BTC", 0.0038)
    account.deposit_currency("ETH", 0.08)
    account.deposit_balance(100)

    account.update_account_value()
    account.starting_value = account.account_value

    t = time.time()
    open_position(account, "BTC")
    open_position(account, "ETH")

    account.print_account_summary()

    trading_results = []
    trading_result = 0

    while time.time() - t < 300:
        positions = account.check_positions()

        for position in positions:
            result = account.close_position(position)
            trading_result += result["result"]
            trading_results.append(trading_result)
            open_position(account, result["currency"])

        #account.print_account_summary()

        time.sleep(5)

    account.close_all_positions()
    account.print_account_summary()
    print("Trading result £{:,.2f}".format(trading_result))
    plot_results(trading_results)


def plot_results(trading_results):
    x = list(range(len(trading_results)))
    plt.plot(x, trading_results)
    plt.xlabel("Trades")
    plt.ylabel("Trading result")

    plt.savefig("graphs/trading_results.png", dpi=1000)


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