'''
Modulo di gestione dei LED

Classi:
 - Led(..)
'''
import machine
import util

class Led:
    '''
    Classe di gestione di un LED semplice.
    
    Metodi:
     - __init__(..)
     - on()
     - off()
    '''
    def __init__(self, pin):
        '''
        Metodo costruttore.
        
        Paramtri:
         - pin -> int : n_pin della scheda 
        '''
        util.Logger.log(f'LED setup at pin: {pin}')
        self.__pin = pin
        
        self.__led = machine.Pin(pin, machine.Pin.OUT)
        self.off()
        
    def off(self):
        '''
        Spegnere il led.
        '''
        self.__led.low()
        
    def on(self):
        '''
        Accendere il led.
        '''
        self.__led.high()
