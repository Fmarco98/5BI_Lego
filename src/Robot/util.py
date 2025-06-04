'''
Util generiche

Classi:
 - Config_schema
 - Logger

Funzioni:
 - errore_led(..)
 - setup_led(..)

'''
import machine
import time
import _thread as threading
import socket

# Variabili globali
LED = None

class Config_schema:
    '''
    Config schema
    
    Elementi:
     - rete
     - mqtt
     - info -> class
     - device -> class
    '''
    rete = None
    mqtt = None
    device = None
    
    class info:
        '''
        Config schema (area "info")
        
        Elementi:
         - relays
         - motori
         - sensori
         - led
         - schede
        '''
        relays = None
        mortori = None
        sensori = None
        led = None
        schede = None
    
    def get_struttura_dict(conf):
        '''
        Parsing della struttura a formato dizionario
        
        Parametri:
         - conf -> Config_schema : config
        
        Ritorna:
         struttura -> dict : struttura formato json
        '''
        return {
            "motori": conf.info.motori,
            "relays": conf.info.relays,
            "sensori": conf.info.sensori,
            "led": conf.info.led,
            "schede": conf.info.schede 
        }
    
class Logger:
    '''
    Classe statica logger.
    
    Funzioni:
     - log(..)
    '''
    def log(msg):
        '''
        Log di un messaggio.
        
        Parametri:
         - msg -> str : messaggio
        '''
        (aaaa, mm, dd, h, m, s, wd, yd) = time.localtime()
        print(f'[{dd}/{mm}/{aaaa}-{h}:{m}:{s}][thread-{threading.get_ident()}]: {msg}')

def setup_led(pin):
    '''
    Setup del led
    
    Parametri:
     - led -> int : pin del led
    '''
    global LED
    
    LED = machine.Pin(pin, machine.Pin.OUT)
    LED.off()

def errore_led(id):
    '''
    Segnalazione tramite led di un errore.
    Tipi di errori:
     - led fisso: errore generico [id: -1]
     - 1 e 2 lampeggi: problemi di rete
     - 9 lampeggi: file json manchanti o non validi [id: 9]
    
    Parametri:
     - id -> int : numero indenticifativo dell'errore
    '''
    print(f'Errore: {id}') 
    
    if id <= -1:
        LED.on()
        print('errore generico')
        while True:
            pass
    else:
        while True:
            # Lampeggio
            for i in range(id):
                LED.on()
                time.sleep(0.2)
                LED.off()
                time.sleep(0.2)
            time.sleep(2)