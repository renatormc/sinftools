
import os
import config
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from sinf_requests import Requester
from requests.exceptions import ConnectionError
from .helpers import get_contact_name

token = os.getenv("SINFBOT_TOKEN")
updater = Updater(token, use_context=True)
dp = updater.dispatcher
bot = Bot(token=token)

requester = Requester(config.SINF_TOKEN)
commands_available = ["/chatid", "/listar", "/liberar", "/bloquear"]


def get_chat_id(update, context):
    user = update.message.from_user
    msg = f"Seu id do seu chat é: {update.message.chat_id}"
    update.message.reply_text(msg)


def send_unknow_message(update, context):
    user = update.message.from_user
    update.message.reply_text(
        "Desculpe, não entendi. Eu só entendo alguns comandos e mensagens e específicas.")


def list_commands(update, context):
    update.message.reply_text("\n".join(commands_available))


def release_server(update, context):
    user = update.message.from_user
    try:
        print(update.message.chat_id)
        contact_name = get_contact_name(update.message.chat_id)
        if not contact_name:
            update.message.reply_text(
                "Desculpe mas não te conheço. Você não está cadastrado.")
            return
        server = config.servers[context.args[0]]
        url = f"{server['url']}/block-server"
        requester.get(url, timeout=5)
        update.message.reply_text(url)
    except ConnectionError:
        update.message.reply_text(
            f"O servidor {context.args[0]} não respondeu")
        return
    except KeyError:
        update.message.reply_text("Servidor desconhecido")
        return
    except IndexError:
        update.message.reply_text("Você não informou o servidor")
        return


def block_server(update, context):
    user = update.message.from_user
    try:
        print(update.message.chat_id)
        contact_name = get_contact_name(update.message.chat_id)
        if not contact_name:
            update.message.reply_text(
                "Desculpe mas não te conheço. Você não está cadastrado.")
            return
        server = config.servers[context.args[0]]
        url = f"{server['url']}/block-server/{contact_name}"
        requester.get(url, timeout=5)
        update.message.reply_text(url)
    except ConnectionError:
        update.message.reply_text(
            f"O servidor {context.args[0]} não respondeu")
        return
    except KeyError:
        update.message.reply_text("Servidor desconhecido")
        return
    except IndexError:
        update.message.reply_text("Você não informou o servidor")
        return


dp.add_handler(CommandHandler('chatid', get_chat_id))
dp.add_handler(CommandHandler('liberar', release_server))
dp.add_handler(CommandHandler('bloquear', block_server))
dp.add_handler(CommandHandler('listar', list_commands))
# dp.add_handler(MessageHandler(Filters.text, send_unknow_message))

if __name__ == "__main__":
    updater.start_polling()
    updater.idle()
