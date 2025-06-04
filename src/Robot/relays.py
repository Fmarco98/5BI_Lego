'''
Modulo dei relays (Relè)

Contenuto
 - class: VoidRelayException
 - class: Relay_3
'''
import machine

class VoidRelayException(Exception):
    '''
    Errore Generato dall'uso di un relay non allocato
    '''
    def __init__(self):
        '''
        Metodo costruttore
        '''
        super().__init__('Pin relay non in uso')

class Relay_3:
    '''
    Classe che raffigura 4 relay
    
    Costanti:
     - States
     - Components
    
    Metodi:
     - costruttore(..)
     - set_state(..)
     - all_off()
    
    '''
    class States:
        '''
        Stati di un relay.
        
        Stati:
         - ON
         - OFF
        '''
        ON = 1
        OFF = 0
    
    class Components:
        '''
        Componenti del relay.
        
        Componenti:
         - R1
         - R2
         - R3
        '''
        R1 = 0
        R2 = 1
        R3 = 2
    
    def __init__(self, r1_pin, r2_pin=-1, r3_pin=-1):
        '''
        Metodo costruttore.
        
        Parametri:
         - r1_pin -> int : pin di controllo del relay 1
         - r2_pin -> int : pin di controllo del relay 2
         - r3_pin -> int : pin di controllo del relay 3
        '''
        self.__relay_pins = (r1_pin, r2_pin, r3_pin)
        self.__relays = [None, None, None]
        
        # Allocazione dei relay
        for pin in self.__relay_pins:
            if pin != -1:
                i = self.__relay_pins.index(pin)
                self.__relays[i] = machine.Pin(pin, machine.Pin.OUT)
        
        self.all_off()

    def set_state(self, relay, stato):
        '''
        Imposta il nuovo stato del relay:
        
        Parametri:
         - relay -> Relay_3.Components : numero del relay
         - stato -> Relay_3.States : nuovo stato
        '''
        # Controllo Se il relay non è allocato
        if not self.__relays[relay]:
            raise VoidRelayException()   
        
        if self.Components.R1 == relay or self.Components.R2 == relay:  
            stato = not stato
            
        self.__relays[relay].value(stato)
    
    def all_off(self):
        '''
        Spegnimeto di tutti i relay.
        '''
        for relay in self.__relays:
            if relay:
                stato = self.States.OFF
                
                if self.__relays[self.Components.R1] == relay or self.__relays[self.Components.R2] == relay:  
                    stato = not stato
            
                relay.value(stato)