import os, logging
from functools import wraps

from telegram.ext import Updater, CommandHandler, RegexHandler
from telegram import ReplyKeyboardMarkup, ChatAction
import docker as docker_api

bot_token = os.environ['BOT_TOKEN']
allowed_users = [int(user_id) for user_id in os.environ['ALLOWED_USERS'].split(',')]

updater = Updater(bot_token)
dispatcher = updater.dispatcher

docker = docker_api.DockerClient(base_url='unix://var/run/docker.sock')

def authorized(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in allowed_users:
            update.message.reply_text('It looks like you aren\'t allowed to do that. '
                                      'Try adding your user ID `{}` to `ALLOWED_USERNAMES`.'.format(update.message.from_user.id),
                                       parse_mode='markdown') 
            return
        return func(bot, update, *args, **kwargs)
    return wrapped

def loading(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        bot.send_chat_action(chat_id=update.effective_user.id, action=ChatAction.TYPING)
        return func(bot, update, *args, **kwargs)
    return wrapped

def help(bot, update):
    reply_text = '*Commands*\n`'
    
    with open('commands.txt', 'r') as f:
        reply_text += f.read()
        reply_text += '`'

    update.message.reply_text(reply_text,
                              parse_mode='markdown')

@loading
@authorized
def info(bot, update):
    containers = docker.containers.list()

    rows = []
    for container in containers:
        rows.append([container.id[:12] + ' - ' + container.name])

    keyboard = ReplyKeyboardMarkup(rows, resize_keyboard=True, one_time_keyboard=True)
    bot.send_message(chat_id=update.effective_user.id, text="Select a container", reply_markup=keyboard)

'''
def info_callback(bot, message):
    if update.message.from_user.id in allowed_users:
        print('hello')
        update.message.reply_text('getting info')
    else:
        update.message.reply_text('It looks like you aren\'t allowed to do that. '
                                  'Try adding your user ID `{}` to `ALLOWED_USERNAMES`.'.format(update.message.from_user.id),
                                  parse_mode='markdown')
'''

@loading
@authorized
def ps(bot, update):
    running_containers = docker.containers.list(filters={'status': 'running'})

    reply_text = '`ID              NAME            IMAGE'
    for container in running_containers:
        reply_text += '\n{}    {}    {}'.format(container.id[:12],
                                                        container.name[:12].ljust(12),
                                                        container.image.tags[0][:32].ljust(12))
    reply_text += '`'

    update.message.reply_text(reply_text,
                                parse_mode='markdown')

@loading
@authorized
def containers(bot, update):
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

@loading
@authorized
def images(bot, update):
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


updater.dispatcher.add_handler(CommandHandler('start', help))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('info', info))
updater.dispatcher.add_handler(CommandHandler('ps', ps))
updater.dispatcher.add_handler(CommandHandler('containers', containers))
updater.dispatcher.add_handler(CommandHandler('images', images))

# updater.dispatcher.add_handler(RegexHandler('[a-f0-9]{12} - [a-zA-Z0-9_]+', info_callback))

print("Starting bot")

updater.start_polling()
updater.idle()