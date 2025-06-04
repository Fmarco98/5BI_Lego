'''
Modulo di gestione dei file json.

Funzioni:
 - config_load(..)
 - prepare_out_json(..)
'''
import json
import utime

import util

def config_load(filepath):
    '''
    Caricamento del config.
    
    Parametri:
     - filepath -> str : file
    
    Ritorna:
     - conf -> util.Config_schema : config
    '''
    conf = util.Config_schema()
    
    conf_file = open(filepath, 'r', encoding='utf-8')
    conf_dict = json.load(conf_file)
        
    conf.device = conf_dict['device']
    conf.rete = conf_dict['rete']
    conf.mqtt = conf_dict['mqtt']
    conf.info.sensori = conf_dict['info']['sensori']
    conf.info.led = conf_dict['info']['led']
    conf.info.relays = conf_dict['info']['relays']
    conf.info.motori = conf_dict['info']['motori']
    conf.info.schede = conf_dict['info']['schede']
        
    conf_file.close()
    return conf

def prepare_out_json(q, q_tot, seriale_msg, id_sender, tipo, desc = "descrizione mancante", struttura = {}, stato = 0):
    '''
    Forma il json di invio.
    
    Parametri:
     - q -> float/int : quantita scavata
     - q_tot -> float/int : quantita scavata totale
     - seriale_msg -> int : seriale messaggio
     - id_sender -> str : id del mittente
     - tipo -> str : tipo del dispositivo mittente
     - desc -> str : descrizione del dispositivo mittente
     - struttura -> dict : struttura componenti
     - stato -> int : stato di autodiagnostica
     
    Ritrona:
     - json -> str : json serializzato
    '''
    json_dict = {
        "tipo": "misura",
        "payload": {
            "quantita": q,
            "quantita_tot": q_tot,
            "seriale": seriale_msg,
            "timestamp": utime.time()
        },
        "sender": {
            "nome": id_sender,
            "tipo": tipo,
            "descrizione": desc,
            "struttura": __parse_struttura(struttura),
            "stato": stato
        }
    }
    
    return json.dumps(json_dict)

def __parse_struttura(struttura):
    '''
    Cropper del dict di struttura per eliminare i pins.
    
    Parametri:
     - struttura -> dict : struttura
    
    Ritorna:
     - cropped_struttura -> dict : struttra senza pins
    '''
    c_struttura = dict()
    
    for gruppo, valore in struttura.items():
        c_gruppo = []
        
        for e in valore:
            c_gruppo.append({
                'nome': e['nome'],
                'tipo': e['tipo']
            })
        
        c_struttura[gruppo] = c_gruppo
    
    return c_struttura