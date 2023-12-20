## TON Smart Challenge Bot

Bot example: [@smartchallenge_example_bot](https://t.me/smartchallenge_example_bot)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/nessshon/smartchallenge-bot.git
    ```

2. Change into the bot directory:

    ```bash
    cd smartchallenge-bot
    ```
3. Clone environment variables file:

   ```bash
   cp .env.example .env
   ```

4. Configure [environment variables](#environment-variables-reference) variables file:

   ```bash
   nano .env
   ```

5. Running a bot in a docker container:

   ```bash
   docker-compose up --build
   ```

## Environment Variables Reference

Here is a reference guide for the environment variables used in the project:

| Variable                 | Type | Description                                                   | Example         |
|--------------------------|------|---------------------------------------------------------------|-----------------|
| BOT_TOKEN                | str  | Bot token, obtained from [@BotFather](https://t.me/BotFather) | 123456:qweRTY   | 
| BOT_DEV_ID               | int  | User ID of the bot developer                                  | 123456789       |
| TON_CONNECT_MANIFEST_URL | str  | tonconnect manifest URL                                       | https://...json |
| REDIS_HOST               | str  | The hostname or IP address of the Redis server                | redis           |
| REDIS_PORT               | int  | The port number on which the Redis server is running          | 6379            |
| REDIS_DB                 | int  | The Redis database number                                     | 1               |
| MYSQL_HOST               | str  | The hostname or IP address of the database server             | localhost       |
| MYSQL_PORT               | int  | The port number on which the database server is running       | 3306            |
| MYSQL_USER               | str  | The username for accessing the database                       | user            |
| MYSQL_PASSWORD           | str  | The password for accessing the database                       | password        |
| MYSQL_DATABASE           | str  | The name of the database                                      | dbname          |
