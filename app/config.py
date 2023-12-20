from dataclasses import dataclass

from environs import Env


@dataclass
class BotConfig:
    TOKEN: str
    DEV_ID: int


@dataclass
class RedisConfig:
    HOST: str
    PORT: int
    DB: int

    def dsn(self) -> str:
        """
        Generates a Redis connection DSN (Data Source Name) using the provided host, port, and database.

        :return: The generated DSN.
        """
        return f"redis://{self.HOST}:{self.PORT}/{self.DB}"


@dataclass
class DatabaseConfig:
    USERNAME: str
    PASSWORD: str
    DATABASE: str
    HOST: str
    PORT: int

    def url(self, driver: str = "mysql+aiomysql") -> str:
        """
        Generates a database connection URL using the provided driver, username, password, host, port, and database.

        :param driver: The driver to use for the connection. Defaults to "mysql+aiomysql".
        :return: The generated connection URL.
        """
        return f"{driver}://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"


@dataclass
class TONConnectConfig:
    MANIFEST_URL: str


@dataclass
class Config:
    bot: BotConfig
    redis: RedisConfig
    database: DatabaseConfig
    tonconnect: TONConnectConfig


def load_config() -> Config:
    env = Env()
    env.read_env()

    return Config(
        bot=BotConfig(
            TOKEN=env.str("BOT_TOKEN"),
            DEV_ID=env.int("BOT_DEV_ID"),
        ),
        redis=RedisConfig(
            HOST=env.str("REDIS_HOST"),
            PORT=env.int("REDIS_PORT"),
            DB=env.int("REDIS_DB"),
        ),
        database=DatabaseConfig(
            HOST=env.str("MYSQL_HOST"),
            PORT=env.int("MYSQL_PORT"),
            USERNAME=env.str("MYSQL_USER"),
            PASSWORD=env.str("MYSQL_PASSWORD"),
            DATABASE=env.str("MYSQL_DATABASE"),
        ),
        tonconnect=TONConnectConfig(
            MANIFEST_URL=env.str("TON_CONNECT_MANIFEST_URL")
        )
    )
