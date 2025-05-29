'''
Modulo di utilià generiche

Funzioni:
 - int_input(..)
 - get_next_day(..)
 - get_timestamp(..)
'''
import datetime
import threading

"""
def int_input(msg=''):
    '''
    Funzione per input interi

    Paramtri:
     - msg -> str : messaggio
    Ritorna:
     - n -> int : numero
    '''
    while True:
        try:
            string = input(msg)
            return int(string)
        except:
            print('\t[Errore] il valore deve essre numerico')
            print('\tReinserisci: ', end='')

def get_next_day(timestamp):
    '''
    Funzione per calcolare il prossomo giono

    Parametri: 
     - timestamp -> timestamp : giono
    Ritorna:
     - timestamp -> timestamp : prossimo giorno
    '''
    data = datetime.datetime.fromtimestamp(timestamp)
    prossima_data = data + datetime.timedelta(days=1)
    return prossima_data.timestamp()

def get_timestamp(aaaa, mm, gg):
    '''
    Funzione per tradurre una data stringa in timestamp

    Parametri:
     - aaaa -> str : anno
     - mm -> str : mese
     - gg -> str : giorno
    Ritorna:
     - timestamp
    '''
    data_string = f'{aaaa}-{mm}-{gg}'
    data = datetime.datetime.fromisoformat(data_string)
    return data.timestamp()
"""

class Logger:
    '''
    Classe statica logger

    Funzioni:
     - log(..)
    '''
    def log(msg):
        '''
        Log di un messaggio
        '''
        str_time = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        print(f'[{str_time}][thread-{threading.get_ident()}]: {msg}')

class Config_schema:
    mqtt = None
    db = None
    
    class device:
        k_chiave = None