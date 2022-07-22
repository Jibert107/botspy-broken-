import socket
import logging 
from emoji import demojize
import re
import sqlite3

class BotSpyClass:

    _serveur = 'irc.chat.twitch.tv'
    _port= 6667

    def __init__(self,token,username,channel) -> None:
        self.__sock = socket.socket()
        self.__sock.connect((self._serveur, self._port))
        self.__sock.send(f"PASS {token}\r\n".encode('utf-8'))
        self.__sock.send(f"NICK {username}\r\n".encode('utf-8'))
        self.__sock.send(f"JOIN {channel}\r\n".encode('utf-8'))
        pass

    def Spy_everythings(self):
        connection = sqlite3.connect("botspy/DBbotspy")#on se connecte a la base de donnée
        curseur = connection.cursor() #variable qui permet de selectiionner un element de la db
        try:
            while True:

                resp = self.__sock.recv(2048).decode('utf-8')
            

                if resp.startswith('PING'):
                    # sock.send("PONG :tmi.twitch.tv\n".encode('utf-8'))
                    self.__sock.send("PONG\n".encode('utf-8'))
                elif len(resp)> 0:
                
                    logging.info(demojize(resp))

                    resp = resp.split('—')[1:]
                    resp = '—'.join(resp).strip()
            
                    matches = re.search(':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', resp)
                    if matches is not None:
                        username, channel, chat_message = matches.groups()
                        # La fonction curseur.execute prend en param pour les values 
                        # un iterable donc [valeur1, valeur2, valeur3] et pas (valeur1, valeur2, valeur3)
                        # Et en plus tu set un ID que le moteur SQL se démerde à faire tout seul
                        nv_message = (curseur.lastrowid, username, chat_message)
                        # Tu oublies de mapper les champs que tu veux peupler avec 
                        # tes values (la base sait surement pas quoi mettre dans quoi)
                        curseur.execute('INSERT INTO botspy_messages VALUES(?,?,?)', nv_message)
                        connection.commit()
                    
                    
                
                    
                    

        except KeyboardInterrupt:
            self.__sock.close()
            connection.close()
            exit()

    def Create_handlers(self):
        logging.basicConfig(level=logging.DEBUG,format='%(asctime)s — %(message)s',datefmt='%Y-%m-%d_%H:%M:%S',handlers=[logging.FileHandler('uwu.log', encoding='utf-8')])

    def __del__(self):
        self.__sock.close()


    
        

