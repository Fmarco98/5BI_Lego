'''
Modulo di gestione dei motori DC.

Classi:
 - Motor(..)
'''
import machine
import util

class Motor:
    '''
    Clase di gestione di un motore DC, interfacciato con H-Bridge (L298-N)
    '''
    class Motion:
        '''
        Enum del movimenti possibili
        '''
        BREKE = (1, 1)
        COAST = (0, 0)
        ORARIO = (1, 0)
        ANTIORARIO = (0, 1)
    
    def __init__(self, inA_pin, inB_pin, EN_pin = -1):
        '''
        Metodo costruttore.
        
        Parametri:
         - inA -> int : pin del inA
         - inB -> int : pin del inB
         - [ EN -> int : pin del EN ]
        '''
        self.__inA_pin = inA_pin
        self.__inB_pin = inB_pin
        self.__EN_pin = EN_pin
        
        util.Logger.log(f'Motor setup at pins: A:{inA_pin}, B:{inB_pin}, EN:{EN_pin}')
        
        self.__inA = machine.Pin(inA_pin, machine.Pin.OUT)
        self.__inB = machine.Pin(inB_pin, machine.Pin.OUT)
        
        if self.__EN_pin != -1:
            self.__EN = machine.PWM(machine.Pin(EN_pin, machine.Pin.OUT))
            self.__EN.freq(1000)
        else:
            self.__EN = None
    
    def set_speed(self, v):
        '''
        Impostare la velocità (se EN abilitato).
        
        Parametri:
         - v -> float : velocità in percentuale [0.0 -> 1.0] 
        '''
        if self.__EN:
            self.__EN.duty_u16(int(65535 * v))
    
    def set_motion(self, tipo):
        '''
        Impostare il movimento.
        
        Parametri:
         - tipo -> Motor.Motion : movimento da eseguire 
        '''
        self.__inA.value(tipo[0])
        self.__inB.value(tipo[1])
            
