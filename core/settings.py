from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int


@dataclass
class Company:
    name: str
    site: str
    offer: str
    start_parameter: str
    logo: str


@dataclass
class Wallet:
    token: str


@dataclass
class Db:
    db_user: str
    db_password: str
    db_database: str
    db_host: str
    db_port: int


@dataclass
class Settings:
    bots: Bots
    company: Company
    wallet: Wallet
    db: Db


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str('TOKEN'),
            admin_id=env.int('ADMIN_ID')
        ),
        company=Company(
            name=env.str('COMPANY_NAME'),
            site=env.str('COMPANY_WEBSITE'),
            offer=env.str('OFFER_LINK'),
            start_parameter=env.str('START_PARAMETER'),
            logo=env.str('LOGO'),
        ),
        wallet=Wallet(
            token=env.str('LIQPAY_TOKEN')
        ),
        db=Db(
            db_user=env.str('DB_USER'),
            db_password=env.str('DB_PASSWORD'),
            db_database=env.str('DB_DATABASE'),
            db_host=env.str('DB_HOST'),
            db_port=env.int('DB_PORT')
        )
    )


settings = get_settings('input')
