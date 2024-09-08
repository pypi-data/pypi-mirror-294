# Linux authentication log (auth.log) monitor and commands executor

## Install
Make dir and creane venv

    $ sudo mkdir -p /opt/apps/logmon
    $ sudo python3 -m venv /opt/apps/logmon/

Install package in venv

    $ sudo /opt/apps/logmon/bin/python3 -m pip install logmon


## Init telegram
    $ cd /opt/apps/logmon && sudo ./bin/python3 -m logmon.init
Initialise telegram bot token and admin chat id

## Run log monitor in command line (for test)
    $ cd /opt/apps/logmon && sudo ./bin/python3 -m logmon.main_watcher
Read /var/log/auth.log and send events to admin telegram

## Run commands executor in command line (for test)
    $ cd /opt/apps/logmon && sudo ./bin/python3 -m logmon.main_executor

Read commands from admin chat

    /stat - show system cpus load and memory usage
    
    /run args - run command from args and return response
    
    /rb - reboot

    /sd - shutdown

## Run log monitor as service

Create and edit .service file

    $ sudo nano /etc/systemd/system/logmon-watcher.service

Paste

    [Unit]
    Description=Logmon-watcher
    After=network.target

    [Service]
    Environment=VIRTUAL_ENV=/opt/apps/logmon
    Environment=PYTHONPATH=/opt/apps/logmon
    ExecStart=/opt/apps/logmon/bin/python3 -m logmon.main_watcher
    Restart=always
    RestartSec=60

    [Install]
    WantedBy=multi-user.target

Enable and start service

    $ sudo systemctl enable logmon-watcher.service
    $ sudo systemctl start logmon-watcher.service


## Run commands executor as service
    $ sudo nano /etc/systemd/system/logmon-executor.service

Paste

    [Unit]
    Description=Logmon-executor
    After=network.target

    [Service]
    Environment=VIRTUAL_ENV=/opt/apps/logmon
    Environment=PYTHONPATH=/opt/apps/logmon
    ExecStart=/opt/apps/logmon/bin/python3 -m logmon.main_executor
    Restart=always
    RestartSec=60

    [Install]
    WantedBy=multi-user.target

Enable and start service

    $ sudo systemctl enable logmon-executor.service
    $ sudo systemctl start logmon-executor.service

# Uninstall

    $ sudo systemctl stop logmon-watcher.service ; sudo systemctl disable logmon-watcher.service ; sudo rm /etc/systemd/system/logmon-watcher.service
    
    $ sudo systemctl stop logmon-executor.service ; sudo systemctl disable logmon-executor.service ; sudo rm /etc/systemd/system/logmon-executor.service
