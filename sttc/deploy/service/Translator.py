'''
Created on Feb 8, 2017

@author: Static
'''
from sttc.deploy.service import Messages as m

class Translator(object):
    '''
    It will be used to translate messages, and actions from the user
    Here we manage i18n, in input we have the key and we decide which value to provide back
    '''


    def __init__(self, userLan):
        self.lan = userLan
        
    def getMessage(self, key):
        try:
            return m.LanguageToMessages[self.lan][key]
        except KeyError:
            return key
        

