#!/usr/bin/python
import sys
# for send bot telegram
import requests
import configparser
import pathlib

class TelegramBot:
    def __init__(self, message, cc=None):
        msg = str(message)
        # panggil config() terlebih dahulu
        self.config()
        # jika cc kosong
        if cc is None:
            cc = self._cc

        self._msg = msg + "\n" + cc
        self.sendMessage()

    def sendMessage(self):
        send_text = self._api_base_url  + self._token + '/sendMessage?chat_id=' + self._chatid + '&parse_mode=HTML&text=' + self._msg

        self.response = requests.get(send_text)

    def config(self):
        try:
            config = configparser.ConfigParser()
            config_file_name = pathlib.Path(__file__).parent.absolute() / "config.ini"
            config.read(config_file_name)
            self._token = config["tele"]["token"]
            self._chatid = config["tele"]["chat_id"]
            self._api_base_url = config["tele"]["api_base_url"]
            self._cc = config["tele"]["cc"]
        except Exception as e:
            print("Error reading file " + config_file_name)
            sys.exit(1)