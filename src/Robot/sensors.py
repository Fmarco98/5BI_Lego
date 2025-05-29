import machine

class Ky032:
    
    def __init__(self, pin, azione):
        self.__pin = pin
        self.on_rilevazione = azione
        self.__flag = False
        
        self.__segnale = machine.Pin(pin, machine.Pin.IN)
        self.id = 0
    
    def check(self):
        valore = self.__segnale.value()
        
        if not valore:
            if not self.__flag:
                self.__flag = True
                self.on_rilevazione()
        else:
            self.__flag = False
