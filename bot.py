import os, logging

from telegram.ext import Updater, CommandHandler
import docker as docker_api

bot_token = os.environ['BOT_TOKEN']
allowed_users = [int(user_id) for user_id in os.environ['ALLOWED_USERS'].split(',')]

updater = Updater(bot_token)
dispatcher = updater.dispatcher

docker = docker_api.DockerClient(base_url='unix://var/run/docker.sock')

def help(bot, update):
    reply_text = '*Commands*\n`'
    
    with open('commands.txt', 'r') as f:
        reply_text += f.read()
        reply_text += '`'

    update.message.reply_text(reply_text,
                              parse_mode='markdown')

def ps(bot, update):
    if update.message.from_user.id in allowed_users:
        running_containers = docker.containers.list(filters={'status': 'running'})

        reply_text = '`ID              NAME            IMAGE'
        for container in running_containers:
            reply_text += '\n{}    {}    {}'.format(container.id[:12],
                                                          container.name[:12].ljust(12),
                                                          container.image.tags[0][:32].ljust(12))
        reply_text += '`'

        update.message.reply_text(reply_text,
                                  parse_mode='markdown')
    else:
        update.message.reply_text('It looks like you aren\'t allowed to do that. '
                                  'Try adding your user ID `{}` to `ALLOWED_USERNAMES`.'.format(update.message.from_user.id),
                                  parse_mode='markdown')

updater.dispatcher.add_handler(CommandHandler('start', help))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('ps', ps))

print("Starting bot")

updater.start_polling()
updater.idle()