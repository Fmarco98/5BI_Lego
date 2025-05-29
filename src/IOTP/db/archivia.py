'''
Salvataggio sul file

Metodi:
 - set_db_collezione(..)
 - archivia(..)
'''
import db_manager as db

DB_COLLEZIONE = ''

def set_db_collezione(collezione):
    '''
    Impostare la collezione di salvataggio file

    Parametri:
     - collezione -> str : nome collezione 
    '''
    global DB_COLLEZIONE

    DB_COLLEZIONE = collezione

def archivia(msg):
    '''
    Archivia la stringa

    Parametri:
     - msg -> str : string da archiviare
    '''

    # Salvataggio su database
    db.insert(msg, DB_COLLEZIONE)