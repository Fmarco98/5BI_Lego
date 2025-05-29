'''
Contiene l'algoritmo di criptazione dei dati.
'''

def get_full_key(key, msgLen):
    '''
    Ottiene la chiave completa.
    
    Parametri:
     - key: chiave
     - msgLen: lunghezza necessaria
     
    Ritorna:
     - full_key: chiave di lunghezza pari a msgLen
    '''
    fullKey = ''
    for i in range(msgLen//len(key)):
        fullKey += key
    fullKey += key[: msgLen - len(fullKey)]
    
    return fullKey

def xor(msg, key):
    '''
    Effettua la criptazione e la decriptazione del messaggio
    
    Parametri:
     - msg: messaggio
     - key: chiave
     
    Ritorna:
     - messaggio criptato
    '''
    full_key = get_full_key(key, len(msg))
    
    criptato = ''
    for i in range(len(msg)):
        criptato += chr(ord(msg[i]) ^ ord(full_key[i]))  # Operazione di XOR binaria
        
    return criptato

def criptazione(payload, key):
    '''
    Cripta il messaggio secondo la chiave key
    
    Parametri:
     - payload: messaggio
     - key: chiave
     
    Ritorna:
     - messaggio criptato
    '''
    return xor(payload, key)
    
def decriptazione(payload, key):
    '''
    Decripta il messaggio secondo la chiave key
    
    Parametri:
     - payload: messaggio criptato
     - key: chiave
     
    Ritorna:
     - messaggio in chiaro
    '''
    return xor(payload, key)
