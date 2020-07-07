from sinfbot import updater
from multiprocessing import Process
from app import app
import config


def keep_checking_telegram():
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    # updater.idle()

def run_flask():
    app.run(host='0.0.0.0', port=config.local_config['port'], debug=config.local_config['debug'])

if __name__ == "__main__":
    keep_checking_telegram()
    run_flask()
    # p = Process(target=keep_checking_telegram)
    # p.start()
    # p2 = Process(target=run_flask)
    # p2.start()
    # p.join()
    # p2.join()