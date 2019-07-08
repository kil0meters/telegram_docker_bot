# Telegram Docker Bot

This is a bot that allows you to manage your docker containers remotely through Telegram.

## Quick Start

Via docker:

```bash
docker run \
  --name=telegram_docker_bot \
  -e BOT_TOKEN=<Token from @BotFather> \
  -e AUTHORIZED_USERS=<Comma separated list of user IDs>
  -v /var/run/docker.sock:/var/run/docker.sock \
  --restart unless-stopped \
  kil0meters/telegram_docker_bot
```

Via docker-compose:

```yaml
version: "3"
services:
  telegram_docker_bot:
    image: "kil0meters/telegram_docker_bot"
    container_name: "telegram_docker_bot"
    environment:
      BOT_TOKEN: "" # Token from @BotFather
      AUTHORIZED_USERS: "" # Comma separated list of user ID's
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
    restart: "unless-stopped"
```

## Generating a bot token

1. Start a chat with `@BotFather`
2. Enter `/newbot`
3. Follow the instructions from there

## Finding your user ID

The bot will tell you your ID if you are not authenticated.