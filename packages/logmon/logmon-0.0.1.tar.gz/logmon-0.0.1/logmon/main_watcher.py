import logging
import time

from .bot import Bot
from .config import Config
from .notify_loop import event_loop_start


def message_send(message_text: str) -> None:
    for chat_id in lm_config.ENV_LOG_CHAT_IDS:
        is_ok = lm_bot.message_send(int(chat_id), message_text, False)
        if not is_ok:
            logging.error(f'Bot message send error for chat id = {chat_id}')


if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)s] {%(module)s:%(lineno)d} %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    
    logging.info('Start')

    lm_config = Config()
    lm_bot = Bot(lm_config.ENV_LOG_BOT_TOKEN, lm_config.ENV_LOG_CHAT_IDS)

    while True:
        try:
            logging.info('Bot monitor start')
            message_send('🚀 Bot monitor start 🚀')
            event_loop_start('/var/log/auth.log', message_send)
        except Exception as ex:
            logging.error('File watch error. Check sudo running.')
            logging.error(str(ex))
        
        time.sleep(60)
