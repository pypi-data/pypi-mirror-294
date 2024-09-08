import pyinotify
import os

EXCLUDE_LIST = [
    'pam_unix(cron:session)',
    'pam_unix(sudo:session)',
]

SIGNS_LIST = {
    'Received disconnect from':'🔒',
    'Disconnected from user':'🔒',
    'Accepted password for':'🔓',
    'Failed password for':'⛔',
    'authentication failure':'⛔',
    'incorrect password attempts':'⛔',
    'Connection reset':'⛔',
    #'✅❌📍📌✉️📩🔐',
}

def event_loop_start(log_path, message_send_func)->None:
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_MODIFY

    handler = EventHandler(log_path, message_send_func)
    notifier = pyinotify.Notifier(wm, handler)

    wm.add_watch(handler.file_path, mask, quiet=False)
    notifier.loop()

def parse_msg(txt:str) -> list[bool, str]:
    log_arr = [x.strip() for x in txt.split(': ')]
    log_arr[0] = [x.strip() for x in log_arr[0].split(' ')]

    # filter
    is_send = True
    for f_el in EXCLUDE_LIST:
        if f_el.lower() == log_arr[1].lower():
            is_send = False
            break
    # format
    log_msg = f'<b>{log_arr[0][2]}</b>\n{log_arr[1]}'
    if len(log_arr)>2:
        log_msg += f'\n{log_arr[2]}'
    if len(log_arr)>3:
        log_msg += f'\n{log_arr[0][0]}'
    
    # sign
    for s_el in SIGNS_LIST:
        if s_el.lower() in log_msg.lower():
            log_msg = SIGNS_LIST[s_el] + ' ' + log_msg
            break

    return [is_send, log_msg]


class EventHandler(pyinotify.ProcessEvent):

    def __init__(self, file_path, message_send_func, *args, **kwargs):
        super(EventHandler, self).__init__(*args, **kwargs)
        self.file_path = file_path
        self._last_position = os.path.getsize(self.file_path)
        self._message_send_func = message_send_func

    def process_IN_MODIFY(self, event):
        if self._last_position > os.path.getsize(self.file_path):
            self._last_position = 0

        with open(self.file_path) as f:
            f.seek(self._last_position)
            log_lines = f.readlines()
            self._last_position = f.tell()
            
            for log_line in log_lines:
                try:
                    res = parse_msg(log_line)
                    if res[0]:
                        self._message_send_func(res[1])
                except Exception as ex:
                    self._message_send_func(f'⛔ {str(ex)}')
                    self._message_send_func(log_line)
