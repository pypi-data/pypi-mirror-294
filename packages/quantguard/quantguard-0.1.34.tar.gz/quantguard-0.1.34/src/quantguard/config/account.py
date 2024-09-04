import toml
from quantguard.config import settings
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


# Define an Account class to store account information
@dataclass
class Account:
    def __init__(
        self, name, tag, exchange, markets, access_key, secret_key, passphrase=None
    ):
        self.name = name
        self.tag = tag
        self.exchange = exchange
        self.markets = markets
        self.access_key = access_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __str__(self):
        return f"Account(name={self.name}, tag={self.tag}, exchange={self.exchange}, markets={self.markets})"


accounts = []


def init_account():
    # Read and parse the TOML file
    with open(settings.SYNC_OMEAGA.config_file, "r") as file:
        config = toml.load(file)

    tmp_accounts = []
    # Extract accounts from the parsed TOML
    for account_data in config.get("accounts", []):
        account = Account(
            name=account_data["name"],
            tag=account_data["tag"],
            exchange=account_data["exchange"],
            markets=account_data["markets"],
            access_key=account_data["access_key"],
            secret_key=account_data["secret_key"],
            passphrase=account_data.get("passphrase"),  # passphrase is optional
        )
        tmp_accounts.append(account)
    sync_account: list = settings.SYNC_OMEAGA.account
    if not sync_account:
        raise ValueError("sync_account is not set in settings")
    for account in tmp_accounts:
        if account.name in sync_account:
            accounts.append(account)
            logger.info(f"Add account: {account}")
