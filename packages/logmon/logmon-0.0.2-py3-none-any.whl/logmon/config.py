import logging
import os

import dotenv


class Config:
    def __init__(self):
        logging.info('Init config')

        self._ENV_FILE = dotenv.find_dotenv()
        if not self._ENV_FILE:
            logging.debug('Not found .env file => Create file')
            with open(".env", "w") as f:
                f.write('ENV_LOG_BOT_TOKEN=\n')
                f.write('ENV_LOG_CHAT_IDS=\n')
            self._ENV_FILE = dotenv.find_dotenv()
        else:
            logging.info('Found .env file')

        dotenv.load_dotenv(self._ENV_FILE)

        self.ENV_LOG_BOT_TOKEN = os.getenv('ENV_LOG_BOT_TOKEN')
        if not self.ENV_LOG_BOT_TOKEN:
            print('BOT TOKEN not fount')
            self.bot_token_input()

        self.ENV_LOG_CHAT_IDS = os.getenv('ENV_LOG_CHAT_IDS')
        if not self.ENV_LOG_CHAT_IDS:
            print('CHAT IDs not fount')
            self.chat_ids_input()

    @property
    def ENV_LOG_BOT_TOKEN(self) -> str | None:
        return self._ENV_LOG_BOT_TOKEN

    @ENV_LOG_BOT_TOKEN.setter
    def ENV_LOG_BOT_TOKEN(self, value: str) -> None:
        self._ENV_LOG_BOT_TOKEN = value
        if value:
            dotenv.set_key(self._ENV_FILE, 'ENV_LOG_BOT_TOKEN', self._ENV_LOG_BOT_TOKEN)
        logging.info(f'BOT TOKEN = {self._ENV_LOG_BOT_TOKEN}')


    @property
    def ENV_LOG_CHAT_IDS(self) -> list[int] | None:
        return self._ENV_LOG_CHAT_IDS

    @ENV_LOG_CHAT_IDS.setter
    def ENV_LOG_CHAT_IDS(self, value: str) -> None:
        self._ENV_LOG_CHAT_IDS = []
        
        if not value:
            return
        
        value_test = str(value)
        dotenv.set_key(self._ENV_FILE, 'ENV_LOG_CHAT_IDS', value_test)
        value_test = value_test.split(';')
        
        for t in value_test:
            if len(t) > 0:
                self._ENV_LOG_CHAT_IDS.append(int(t))
        logging.info(f'CHAT IDs = {self._ENV_LOG_CHAT_IDS}')


    def bot_token_input(self) -> None:
        token_test = input('Enter bot token = ')
        self.ENV_LOG_BOT_TOKEN = ''.join(e for e in token_test if e.isalnum() or e in [':', '_', '-'])

    def chat_ids_input(self) -> None:
        print('Enter chat ids\nexample for one chat: 123123123\nexample for many chats: 123123123;213213213;321321321')
        list_test = input('Chat ids = ')
        self.ENV_LOG_CHAT_IDS = ''.join(e for e in list_test if e.isnumeric() or e in [';'])
