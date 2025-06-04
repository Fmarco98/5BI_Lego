'''
Modulo di gestione dei sensori

Classi:
 - Ky032
'''
import machine

import util

class Ky032:
    '''
    Gestione di sensore Ky-032 (rilevamento di oggetti)
    
    Metodi:
     - __init__(..)
     - check(..)
    '''
    def __init__(self, pin, azione):
        '''
        Metodo costruttore.
        
        Parametri:
         - pin -> int : pin del segnale
         - azione -> function : event handler
        '''
        self.__pin = pin
        
        util.Logger.log(f'Sensor ky-032 setup at pin: {pin}')
        
        self.on_rilevazione = azione
        self.__flag = False
        
        self.__segnale = machine.Pin(pin, machine.Pin.IN)
        self.id = 0
    
    def check(self):
        '''
        Controllo avvenimento di una rilevazione.
        '''
        valore = self.__segnale.value()
        
        if not valore:
            if not self.__flag:
                self.__flag = True
                self.on_rilevazione()
        else:
            self.__flag = False