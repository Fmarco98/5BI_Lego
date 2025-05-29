import machine

class Motor:
    class Motion:
        BREKE = (1, 1)
        COAST = (0, 0)
        ORARIO = (1, 0)
        ANTIORARIO = (0, 1)
    
    def __init__(self, inA_pin, inB_pin, EN_pin = -1):
        self.__inA_pin = inA_pin
        self.__inB_pin = inB_pin
        self.__EN_pin = EN_pin
        
        self.__inA = machine.Pin(inA_pin, machine.Pin.OUT)
        self.__inB = machine.Pin(inB_pin, machine.Pin.OUT)
        
        if self.__EN_pin != -1:
            self.__EN = machine.PWM(machine.Pin(EN_pin, machine.Pin.OUT))
            self.__EN.freq(1000)
        else:
            self.__EN = None
    
    def set_speed(self, v):
        if self.__EN:
            self.__EN.duty_u16(int(65535 * v))
    
    def set_motion(self, tipo):
        self.__inA.value(tipo[0])
        self.__inB.value(tipo[1])
            
