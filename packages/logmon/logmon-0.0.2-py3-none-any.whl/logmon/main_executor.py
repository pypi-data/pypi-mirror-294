import logging
import time

from .bot import Bot
from .config import Config
from .commands_linux import exec_reboot, exec_run, exec_shutdown, exec_status

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

    # Reset previous messages
    lm_bot.chat_id_get_last()

    while True:
        try:
            logging.info('Bot commands start')
            message_send('🚀 Bot commands start 🚀')
            
            while True:
                msgs = lm_bot.updates_get()
                if msgs:
                    for m in msgs:
                        if m['message']['from']['id'] in lm_config.ENV_LOG_CHAT_IDS:
                            match m['message']['text']:
                                case '/sd':
                                    message_send(exec_shutdown())
                                case '/rb':
                                    message_send(exec_reboot())
                                case '/stat':
                                    message_send(exec_status())
                            
                            if '/run' in m['message']['text']:
                                if m['message']['text'].strip() == '/run':
                                    message_send('Empty /run')
                                else:
                                    message_send(exec_run(m['message']['text']))
                time.sleep(5)

        except Exception as ex:
            logging.error('Getting updates error.')
            logging.error(str(ex))
        
        time.sleep(60)

