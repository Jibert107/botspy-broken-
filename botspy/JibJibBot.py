from sqlite3.dbapi2 import Date
from Database import DB
import socket
from emoji import demojize
import re
import datetime

class JibJibBot:
    _server: str = 'irc.chat.twitch.tv'
    _port: int = 6667
    _db: DB

    def __init__(self, token, nickname, channel) -> None:
        self.__sock = socket.socket()
        self.__sock.connect((self._server, self._port))
        self.__sock.send(f"PASS {token}\r\n".encode('utf-8'))
        self.__sock.send(f"NICK {nickname}\r\n".encode('utf-8'))
        self.__sock.send(f"JOIN {channel}\r\n".encode('utf-8'))
        self._db = DB()
        pass

    def listen_to_fucking_chat(self):
        try:
            while True:
                resp = self.__sock.recv(2048).decode('utf-8')

                if resp.find('PING') != -1:
                    self.send('PONG')

                elif len(resp) > 0:
                    self.handle_message(demojize(resp))

        except RuntimeError:
            self.__sock.close()
            exit()

    def __del__(self):
        self.__sock.close()

    def send(self, message: str):
        self.__sock.send(bytes(message.encode("UTF-8")))

    def send_message(self, message: str):
        #TODO : Apprendre à parler sur irc ptdr
        toSend = ("PRIVMSG #fumolol " + message).encode("UTF-8")
        self.__sock.send(bytes(toSend))

    def handle_message(self, message):
        print(message)
        
        matches = re.search(':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', message)
        if matches is not None:
            username, channel, chat_message = matches.groups()
            self._db.insert('messages', ['message_username', 'message_date', 'message_text'], [username, datetime.datetime.now(), chat_message])

    def get_all_fucking_messages(self):
        #return self._db.select("messages", ['message_username']) #exemple avec juste les usernames
        return self._db.select("messages")
