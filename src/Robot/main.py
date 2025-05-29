# PROGETTO ROBOT - ESCAVATORE
# 
# Autore: Casciello Marco, Mattiolo Luca
# Classe: 5BI
# Data di consegna: 
# 
# Descrizione:
#
#
# Nome script: main.py
# Moduli locali: 
import json
import utime
import time

from umqtt.simple import MQTTClient as Mqtt

import wifidc
import util
import movimenti
import cripta
from relays import Relay_3 as Relay
from sensors import Ky032
from motors import Motor

#Variabili globali
CONF = util.Config_schema()
CLIENT_MQTT = None
status = False  # Flase = offline | True = online

SENSORE = None
RELAY = None
MOTORI = dict()
LED = dict()

n_pale = 0

def setup():
    '''
    Setup
    '''
    global CONF, CLIENT_MQTT, SENSORE, MOTORI, LED, RELAY
    
    util.Logger.log('setup iniziato')
    
    '''
    # Azzeramento tutti i GPIO
    for i in range(26):
        pin = machine.Pin(i, machine.Pin.OUT)
        pin.low()
    '''
    
    util.setup_led('LED')
    
    try:
        # Lettura dati dai file
        conf_file = open('config.json', 'r', encoding='utf-8')
        conf_dict = json.load(conf_file)
        
        CONF.device = conf_dict['device']
        CONF.rete = conf_dict['rete']
        CONF.mqtt = conf_dict['mqtt']
        CONF.info.sensori = conf_dict['info']['sensori']
        CONF.info.led = conf_dict['info']['led']
        CONF.info.relays = conf_dict['info']['relays']
        CONF.info.motori = conf_dict['info']['motori']
        
        conf_file.close()
    except Exception as e:
        # Visualizzazzione dell'errore
        print(e)
        util.errore_led(9)
    
    # Allocare motori, sensori, relays
    
    RELAY = Relay(CONF.info.relays[0]['pin']['S'], CONF.info.relays[1]['pin']['S'], CONF.info.relays[2]['pin']['S'])
    SENSORE = Ky032(CONF.info.sensori[0]['pin']['S'], on_rilevazione)
    
    # -----------
    
    # Gestione status WLAN
    wlan_status = wifidc.connetti(CONF.rete['ssid'], CONF.rete['password'])
    if wlan_status != 3:
        util.errore_led(wlan_status)
    
    util.Logger.log('connesso alla WLAN')
    
    #Connessione MQTT
    CLIENT_MQTT = Mqtt(CONF.mqtt['client-id'], CONF.mqtt['broker'], CONF.mqtt['porta'], CONF.mqtt['keepalive'])
    CLIENT_MQTT.set_callback(on_message)
    CLIENT_MQTT.connect()
    util.Logger.log(f'connesso al broker: {CONF.mqtt['broker']}')
    
    CLIENT_MQTT.subscribe(CONF.mqtt['topic_cmd'])
    util.Logger.log(f'sottoscritto al topic: {CONF.mqtt['topic_cmd']}')
    
    util.Logger.log('setup finito')

# --- Funzioni movimenti ------
#@util.motion('avanti')
def avanti_cingoli():
    pass

def indietro_cingoli():
    pass

def destra_cingoli():
    pass

def sinistra_cingoli():
    pass

def stop_cingoli():
    pass

def pistoni_su():
    pass

def pistoni_giu():
    pass

def stop_pistoni():
    pass

def ruota_scarico_destra():
    pass

def ruota_scarico_sinistra():
    pass

def stop_ruota_scarico():
    pass

def start_scava():
    pass

def stop_scava():
    pass

def ruota_torre_destra():
    pass

def ruota_torre_sinistra():
    pass

def stop_ruota_torre():
    pass

def accendi_lego():
    status = True
    RELAY.set_state(Relay.Components.R1, Relay.States.ON)
    RELAY.set_state(Relay.Components.R2, Relay.States.ON)
    RELAY.set_state(Relay.Components.R3, Relay.States.ON)

def spegni_lego():
    status = False
    RELAY.all_off()

# ------------ Eventi ------------------------

def on_message(topic, msg):
    try:
        msg = msg.decode('utf-8')
        msg = cripta.decriptazione(msg, CONF.device['k-chiave'])
        json_msg = json.loads(msg)
    
        util.Logger.log(f'Ricevuto: {msg}')
    
        if json_msg['tipo'] == 'comando':
            azione = json_msg['payload']['azione']
        
            if azione == movimenti.IDs.Cingoli.AVANTI:
                avanti_cingoli()
            
            elif azione == movimenti.IDs.Cingoli.INDIETRO:
                indietro_cingoli()
            
            elif azione == movimenti.IDs.Cingoli.DESTRA:
                destra_cingoli()
            
            elif azione == movimenti.IDs.Cingoli.SINISTRA:
                sinistra_cingoli()
            
            elif azione == movimenti.IDs.Cingoli.STOP:
                stop_cingoli()
        
            elif azione == movimenti.IDs.Pistoni.SU:
                pistoni_su()

            elif azione == movimenti.IDs.Pistoni.GIU:
                pistoni_giu()

            elif azione == movimenti.IDs.Pistoni.STOP:
                stop_pistoni()
            
            elif azione == movimenti.IDs.Scarico.DESTRA:
                ruota_scarico_destra()
            
            elif azione == movimenti.IDs.Scarico.SINISTRA:
                ruota_scarico_sinistra()
            
            elif azione == movimenti.IDs.Scarico.STOP:
                stop_ruota_scarico()
            
            elif azione == movimenti.IDs.Scava.START:
                start_scava()
            
            elif azione == movimenti.IDs.Scava.STOP:
                stop_scava()
            
            elif azione == movimenti.IDs.Torre.DESTRA:
                ruota_torre_destra()
            
            elif azione == movimenti.IDs.Torre.SINISTRA:
                ruota_torre_sinistra()
            
            elif azione == movimenti.IDs.Torre.STOP:
                stop_ruota_torre()
            
            elif azione == movimenti.IDs.Lego.ON:
                accendi_lego()
            
            elif azione == movimenti.IDs.Lego.OFF:
                spegni_lego()
            
            else:
                util.Logger.log('comando errato')
        
    except Exception as e:
        util.Logger.log(f'Ricevimento errato: {e}')
            
def on_rilevazione():
    global n_pale
    n_pale += 1
    
    util.Logger.log('Rilevata pala')

# -----------------------------------

def main():
    '''
    Main dello script
    '''
    global n_pale
    setup()
    
    delay = .05
    tick_per_invio = int(CONF.device['t-invio']*60 / delay)
    tick = 0
    
    while True:
        CLIENT_MQTT.check_msg()
        
        # Rilevazione sensore
        SENSORE.check()
        
        if (status or n_pale > 0) and tick == tick_per_invio:
            json_dict = {
                            "tipo": "misura",
                            "payload": {
                                "quantita": n_pale*CONF.device['volume-pala'],
                                "timestamp": utime.time()
                            },
                            "sender": {
                                "nome": CONF.device['id']
                            }
                        }
            
            msg = json.dumps(json_dict)
            msg_c = cripta.criptazione(msg, CONF.device['k-chiave'])
            CLIENT_MQTT.publish(CONF.mqtt['topic_misure'], msg_c, qos=0)
            util.Logger.log(f'Inviato su {CONF.mqtt['topic_misure']}: {msg}')
            tick = 0
            n_pale = 0
            
        tick += 1
        time.sleep(delay)

try:
    main()
except Exception as e:
    if CLIENT_MQTT:
        CLIENT_MQTT.disconnect()
    
    if RELAY:
        spegni_lego()
    
    print(e)
    util.errore_led(-1)
