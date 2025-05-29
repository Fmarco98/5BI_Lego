# RECEZIONE IOTDATA CON MQTT
# Progetto numero 4
# Autore: Casciello Marco
# Classe: 5BI
# Data di consegna: 
# 
# Descrizione: 
# Lo script è la rappresentazione della IOTP, in un'altra rete, dove si devono salvare 
# i vari dati nel file 'iotp/dbplatform'. Fra la IOTP e il DA vi è una comunicazione MQTT.
# Inoltre, dato che probabilmente sono in due reti diverse, il messaggio ricevuto è criptato.
# Quest'ultimo viene decriptato mediante il moduto 'cripta.py', che è presenta anche nel DA.
#
# Revisione (progetto 5):
# Gli iotdata sono salvati anche sul DB
#
# Nome script: archivia_iotp.py
# Moduli locali: 
#  - cripta.py 
#  - archivia.py 
#  - db_manager.py

import paho.mqtt.client as mqtt
import json
import time

import cripta  # Modulo di decriptazione
import archivia  # Salvataggio su file
import db_manager  # Modulo di interazione col db
import util

# Variablili globali
CONF = util.Config_schema()
client = None

def setup():
    '''
    Funzione di setup del programma.
    La funzione carica i dati dal file di configurazione json,
    o nel caso che non esista ne genera uno di default.
    '''
    global CONF
    
    try:
        # Lettura file di configurazione
        conf_file = open('config.json', 'r', encoding = 'utf-8')
        conf_json = json.load(conf_file)

        CONF.mqtt = conf_json['mqtt']
        CONF.db = conf_json['db']
        CONF.device.k_chiave = conf_json['device']['k-chiave']

        conf_file.close()

    except Exception as e:
        # Gestione se file mancante
        conf_json = {
            "device": {
                "k-chiave": ""
            },
            "mqtt": {
                "keepalive": 0,
                "topic_misure": "",
                "broker": "",
                "porta": 1883,
                "qos": 0
            },
            "db": {
                "uri": "",
                "database": "",
                "collezione_misure": "",
                "collezione_id": ""
            }
        }
        
        conf_file = open('config.json', 'w', encoding='utf-8')
        json.dump(conf_json, conf_file, indent = 4)
        conf_file.close()

        util.Logger.log(f'Errore: {e}')
        
def on_connect(client, user_data, flags, rc, properties):
    '''
    Funzione di Callback dell'evento on_connect.

    Parametri:
     - client
     - user_data
     - flags
     - rc
     - properties
    '''
    
    if rc == 0:
        util.Logger.log(f'Client connessio: {CONF.mqtt["broker"]}:{CONF.mqtt["porta"]} - {CONF.mqtt["topic_misure"]}')
    
        client.subscribe(CONF.mqtt['topic_misure'], CONF.mqtt['qos'])
    else:
        util.Logger.log(f'Errore di connessione: MQTT-rc-flag: {rc}')

def on_message_received(client, user_data, msg):
    '''
    Funzione di Callback dell'evento on_message.

    Parametri:
     - client
     - user_data
     - msg
    '''
    # Decriptazione
    string = cripta.decriptazione(msg.payload.decode('utf-8'), CONF.device.k_chiave)
    util.Logger.log(f'Messaggio ricevuto \n{string}')

    # Salvataggio
    archivia.archivia(string)

def main():
    '''
    Main dello script
    '''
    global client
    
    # Setup del programma
    util.Logger.log('setup start')
    setup()
    util.Logger.log(CONF.db)
    db_manager.setup_db(CONF.db['uri'], CONF.db['database'])
    archivia.set_db_collezione(CONF.db['collezione_misure'])

    #client = mqtt.Client()
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message_received

    util.Logger.log('setup end')

    client.connect(CONF.mqtt['broker'], CONF.mqtt['porta'], CONF.mqtt['keepalive'])
    # mqtt loop
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        pass

    client.disconnect()

# Cotrollo di avvio
if __name__ == '__main__':
    main()