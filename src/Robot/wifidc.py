'''
Modulo dedicato alla connessione ad una WLAN

Funzioni:
 - connetti(..)
'''
import network
import time

def connetti(ssid, password):
    '''
    Connessione ad una rete wireless.
    
    Parametri:
     - ssid: nome rete
     - password: password rete
    Ritorna:
     - status: status della rete
    '''
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Connessione alla rete
    tentativi = 10
    wlan.connect(ssid, password)
    while tentativi > 0:
        tentativi -= 1
        time.sleep(1)
        
        if wlan.status == 3: #Connessione eseguita
            return 3
    
    return wlan.status()
    
