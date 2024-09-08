import logging

from .bot import Bot
from .config import Config


if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)s] {%(module)s:%(lineno)d} %(levelname)s - %(message)s',
                        level=logging.INFO)
    logging.info('Start')

    lm_config = Config()
    lm_bot = Bot(lm_config.ENV_LOG_BOT_TOKEN, lm_config.ENV_LOG_CHAT_IDS)

    # Test bot
    logging.info('Bot token test')
    while not lm_bot.bot_test():
        print('Bot connection error, read logging debug')
        resp = input('Do you want to enter [N]ew bot token: ').lower().strip()
        if len(resp) > 0:
            if resp[0] == 'n':
                lm_config.bot_token_input()
                continue
        exit()

    # Test chat ids
    is_ok_one = False
    logging.info(f'Chat ids test: {lm_config.ENV_LOG_CHAT_IDS}')
    while not is_ok_one:
        for chat_id in lm_config.ENV_LOG_CHAT_IDS:
            logging.info(f'Test {chat_id}')
            is_ok = lm_bot.message_send(int(chat_id), 'Test connection', True)
            if not is_ok:
                print(f'Bot message send error for chat id = {chat_id}')
            else:
                is_ok_one = is_ok

        if not is_ok_one:
            resp = input('Do you want to enter [N]ew IDs  or get [L]ast chat id? ').lower().strip()
            if len(resp) > 0:
                if resp[0] == 'n':
                    lm_config.chat_ids_input()
                    continue
                if resp[0] == 'l':
                    lm_config.ENV_LOG_CHAT_IDS = lm_bot.chat_id_get_last()
                    continue
            exit()

    logging.info('BOT READY')
    logging.info('Run main.py')

