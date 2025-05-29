'''
Util generiche

Classi:
 - Config_schema
 - Logger

Funzioni:
 - errore_led(..)
 - setup_led(..)

Decorators:
 - motion(..)
'''
import machine
import time
import _thread as threading
import socket

# Variabili globali
LED = None

class Config_schema:
    rete = None
    mqtt = None
    
    class info:
        relays = None
        mortori = None
        sensori = None
        led = None
    
    class device:
        k_chiave = None
        t_invio = None
        id = None

class Logger:
    def log(msg):
        '''
        Log di un messaggio
        '''
        (aaaa, mm, dd, h, m, s, wd, yd) = time.localtime()
        print(f'[{dd}/{mm}/{aaaa}-{h}:{m}:{s}][thread-{threading.get_ident()}]: {msg}')

def setup_led(pin):
    '''
    Setup del led
    
    Parametri:
     - led -> pin del led
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
     - id: numero indenticifativo dell'errore
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

def get_IP_from_FQDN(fqdn):
    return socket.gethostbyname(fqdn)

'''
def motion(attivita):
    def decorator(f):
        def wrapper():
            Logger.log(f'inizio attività - {attivita}')
            f()
            Logger.log(f'fine attività - {attivita}')
    
        return wrapper
    return decorator'''