'''
Modulo di gestione del db mongo

Funzioni:
 - setup_db(..)
 - insert(..)
 - select(..)
'''
import json
import pymongo

# Varaibili globali
DB_URI = ''
DB_DB = ''

MONGO_CLIENT = None
MONGO_DB = None

def setup_db(uri, db):
    '''
    Setup del file

    Parametri:
     - uri -> str : stringa di accesso
     - db -> str : nome db
    '''
    global DB_URI, DB_DB, MONGO_CLIENT, MONGO_DB

    # Controllo validità minima dei dati
    if uri == '' or db == '':
        raise Exception('no database')

    DB_DB = db
    DB_URI = uri

    MONGO_CLIENT = pymongo.MongoClient(DB_URI)
    MONGO_DB = MONGO_CLIENT[db]

def insert(stringa, collezione):
    '''
    Funzione di inserimento nel database

    Parametri: 
     - stringa -> str: strigna json
     - collezione -> str: collezione dove salvarlo
    '''
    col = MONGO_DB[collezione]

    data = json.loads(stringa)
    col.insert_one(data)

def select(definizione, collezione):
    '''
    Funzione di selezione dal db

    Parametri:
     - definzione -> dict : condizione e target list
     - collezione -> str : collezione da dove prelevare i dati 
    Ritorna:
     - query
    '''
    col = MONGO_DB[collezione]
    result = col.find(definizione['condizione'], definizione['target'])
    
    return result.to_list()