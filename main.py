import cbpro as cbp
import configparser


def main():
    keys = get_keys("secret/config.txt")
    print(keys)


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