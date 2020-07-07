from sinfbot.app import app
import config

app.run(host='0.0.0.0', port=config.telegram_bot_api_port, debug=config.debug)
