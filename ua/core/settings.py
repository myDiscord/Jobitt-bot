from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str


@dataclass
class Channels:
    channel_id: int
    link: str


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
    channels: Channels
    db: Db


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str('TOKEN')
        ),
        channels=Channels(
            channel_id=env.int('ID'),
            link=env.str('LINK')
        ),
        db=Db(
            db_user=env.str('DB_USER'),
            db_password=env.str('DB_PASSWORD'),
            db_database=env.str('DB_DATABASE'),
            db_host=env.str('DB_HOST'),
            db_port=env.int('DB_PORT')
        )
    )


settings = get_settings('ua/input')
