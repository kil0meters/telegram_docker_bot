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

def containers(bot, update):
    if update.message.from_user.id in allowed_users:
        containers = docker.containers.list()

        reply_text = '`ID              NAME            IMAGE               STATUS'
        for container in containers:
            reply_text += '\n{}    {}    {}    {}'.format(container.id[:12],
                                                          container.name[:12].ljust(12),
                                                          container.image.tags[0][:16].ljust(16),
                                                          container.status)
        reply_text += '`'

        update.message.reply_text(reply_text,
                                  parse_mode='markdown')
    else:
        update.message.reply_text('It looks like you aren\'t allowed to do that. '
                                  'Try adding your user ID `{}` to `ALLOWED_USERNAMES`.'.format(update.message.from_user.id),
                                  parse_mode='markdown')

def images(bot, update):
    if update.message.from_user.id in allowed_users:
        images = docker.images.list()

        reply_text = '`ID              REPOSITORY          TAG         SIZE'
        for image in images:
            try:
                repository = image.tags[0].split(':')[0][:16].ljust(16)
            except:
                repository = '<none>'.ljust(16)

            try:
                tag = image.tags[0].split(':')[1][:8].ljust(8)
            except:
                tag = '<none>'.ljust(8)


            reply_text += '\n{}    {}    {}    {}'.format(image.id[7:][:12],
                                                          repository,
                                                          tag,
                                                          'placeholder')
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
updater.dispatcher.add_handler(CommandHandler('containers', containers))
updater.dispatcher.add_handler(CommandHandler('images', images))

print("Starting bot")

updater.start_polling()
updater.idle()