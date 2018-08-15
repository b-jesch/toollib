import random
import xbmcaddon
ADDON = xbmcaddon.Addon()

class crypt(object):


    def __init__(self, passw, key, token):

        self.passw = ADDON.getSetting(passw)

        self.__pw_item  = passw
        self.__key = ADDON.getSetting(key)
        self.__key_item = key
        self.__token = ADDON.getSetting(token)
        self.__token_item = token


    def persist(self):
        ADDON.setSetting(self.__key_item, self.__key)
        ADDON.setSetting(self.__token_item, self.__token)
        ADDON.setSetting(self.__pw_item, '*')


    def crypt(self):
        '''
        :param pw: ID/Name of the associated password item in settings.xml
        :param key: ID of the associated key in settings, will be generated at first run
        :param token: ID of the token in settings, generated from password/key
        :return: decrypted password if password in settings is empty or *, else set password to '*' and generates key/token,
                 stores password into settings.xml, key/token within userdata/addon_data/addon_id/settings.xml

        example: crypt('addon_password', 'key', 'token') reads password from item 'addon_password' in settings.xml.
        If password is '*', returns with the decrypted password calculated from key/token, otherwise a given password
        is set to '*' and a key and token is generated and stored.
        '''

        if self.passw == '' or self.passw == '*':
            if len(self.__key) > 2: return "".join([chr(ord(self.__token[i]) ^ ord(self.__key[i])) for i in range(int(self.__key[-2:]))])
            return ''
        else:
            self.__key = ''
            for i in range((len(self.passw) / 16) + 1):
                self.__key += ('%016d' % int(random.random() * 10 ** 16))
            self.__key = self.__key[:-2] + ('%02d' % len(self.passw))
            __tpw = self.passw.ljust(len(self.__key), 'a')

            self.__token = "".join([chr(ord(__tpw[i]) ^ ord(self.__key[i])) for i in range(len(self.__key))])
            self.persist()
            return self.passw