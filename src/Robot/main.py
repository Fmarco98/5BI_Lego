# PROGETTO ROBOT - ESCAVATORE
# 
# Autore: Casciello Marco, Mattiolo Luca
# Classe: 5BI
# Data di consegna: 
# 
# Descrizione:
# Automazione di un robot cingolato da miniera
#
# Nome script: main.py
# Moduli locali: wifidc.py, util.py, movimenti.py, cripta.py, relays.py, sensors.py, motors.py, leds.py
import time

from umqtt.simple import MQTTClient as Mqtt

import wifidc
import util
import movimenti
import cripta
import json_manager as jmng
from relays import Relay_3 as Relay
from sensors import Ky032
from motors import Motor
from leds import Led

#Variabili globali
CONF = util.Config_schema()
CLIENT_MQTT = None
status = True  # Flase = offline | True = online

SENSORE = None
RELAY = None
MOTORI = dict()
LED = dict()

n_pale = 0

# --- Funzioni movimenti ------
def avanti_cingoli():
    '''
    Movineto in avanti (se robot acceso).
    '''
    if status:
        util.Logger.log('Movimento:cingoli-avanti')
        MOTORI['C-DX'].set_motion(Motor.Motion.ORARIO)
        MOTORI['C-SX'].set_motion(Motor.Motion.ORARIO)

def indietro_cingoli():
    '''
    Movineto in indietro (se robot acceso).
    '''
    if status:
        util.Logger.log('Movimento:cingoli-indietro')
        MOTORI['C-DX'].set_motion(Motor.Motion.ANTIORARIO)
        MOTORI['C-SX'].set_motion(Motor.Motion.ANTIORARIO)

def destra_cingoli():
    '''
    Rotazione a destra (se robot acceso).
    '''
    if status:
        util.Logger.log('Movimento:cingoli-destra')
        MOTORI['C-DX'].set_motion(Motor.Motion.ANTIORARIO)
        MOTORI['C-SX'].set_motion(Motor.Motion.ORARIO)

def sinistra_cingoli():
    '''
    Rotazione a sinistra (se robot acceso).
    '''
    if status:
        util.Logger.log('Movimento:cingoli-sinistra')
        MOTORI['C-DX'].set_motion(Motor.Motion.ORARIO)
        MOTORI['C-SX'].set_motion(Motor.Motion.ANTIORARIO)

def stop_cingoli():
    '''
    Ferma i cingoli del robot (se robot acceso).
    '''
    if status:
        util.Logger.log('Movimento:cingoli-stop')
        MOTORI['C-DX'].set_motion(Motor.Motion.COAST)
        MOTORI['C-SX'].set_motion(Motor.Motion.COAST)

def pistoni_su():
    '''
    Estendere i pistoni (se robot acceso).
    '''
    if status:
        util.Logger.log('Movimento:pistoni-su')
        MOTORI['Pistoni'].set_motion(Motor.Motion.ANTIORARIO)

def pistoni_giu():
    '''
    Retrarre i pistoni (se robot acceso).
    '''
    if status:
        util.Logger.log('Movimento:pistoni-giu')
        MOTORI['Pistoni'].set_motion(Motor.Motion.ORARIO)

def stop_pistoni():
    '''
    Fermare i pistoni (se robot acceso).
    '''
    if status:
        util.Logger.log('Movimento:pistoni-stop')
        MOTORI['Pistoni'].set_motion(Motor.Motion.COAST)

def ruota_scarico_destra():
    '''
    Ruota il nastro di scarico a destra (se robot acceso).
    '''
    if status:
        util.Logger.log('Movimento:ruota_scarico-destra')
        MOTORI['Scarico'].set_speed(1)
        MOTORI['Scarico'].set_motion(Motor.Motion.ANTIORARIO)
        time.sleep(0.1)
        MOTORI['Scarico'].set_speed(0.9)
        
def ruota_scarico_sinistra():
    '''
    Ruota il nastro di scarico a sinistra (se robot acceso).
    '''
    if status:
        util.Logger.log('Movimento:ruota_scarico-sinistra')
        MOTORI['Scarico'].set_speed(1)
        MOTORI['Scarico'].set_motion(Motor.Motion.ORARIO)
        time.sleep(0.1)
        MOTORI['Scarico'].set_speed(0.8)

def stop_ruota_scarico():
    '''
    Ferma la rotazione del nastro di scarico (se robot acceso).
    '''
    if status:
        util.Logger.log('Movimento:ruota_scarico-stop')
        MOTORI['Scarico'].set_motion(Motor.Motion.COAST)

def start_scava():
    '''
    Inizia estrazione (se robot acceso).
    '''
    if status:
        util.Logger.log('Movimento:scava-avvio')
        MOTORI['Scava'].set_speed(1)
        MOTORI['Scava'].set_motion(Motor.Motion.ORARIO)
        
        MOTORI['Nastro'].set_speed(0.5)
        MOTORI['Nastro'].set_motion(Motor.Motion.ORARIO)
    
def stop_scava():
    '''
    Concludi estrazione (se robot acceso).
    '''
    if status:
        util.Logger.log('Movimento:scava-stop')
        MOTORI['Scava'].set_motion(Motor.Motion.COAST)
        MOTORI['Nastro'].set_motion(Motor.Motion.COAST)

def accendi_lego():
    '''
    Impostare il lego in logicamente acceso.
    '''
    global status
    
    if not status:
        util.Logger.log('Funzione:lego-on')
        status = True
        RELAY.set_state(Relay.Components.R1, Relay.States.ON)
        RELAY.set_state(Relay.Components.R2, Relay.States.ON)
        RELAY.set_state(Relay.Components.R3, Relay.States.ON)
        
        LED['ON'].on()
        LED['OFF'].off()

def spegni_lego():
    '''
    Impostare il lego in logicamente spento.
    '''
    global status
    
    if status:
        util.Logger.log('Funzione:lego-off')
        status = False
        RELAY.all_off()
        
        LED['ON'].off()
        LED['OFF'].on()
    
# ------------ Eventi ------------------------

def on_message(topic, msg):
    '''
    Event handler della recezione messaggio mqtt.
    
    Parametri:
     - topic -> str: topic mqtt
     - msg -> bytes: messaggio
    '''
    try:
        msg = msg.decode('utf-8')
        msg = cripta.decriptazione(msg, CONF.device['k-chiave'])
        json_msg = json.loads(msg)
    
        util.Logger.log(f'Ricevuto:\n{msg}')
    
        if json_msg['tipo'] == 'comando':
            
            # Selezione comando
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
    '''
    Event handler della rilevazione del sensore.
    '''
    global n_pale
    n_pale += 1
    
    util.Logger.log('Rilevata pala')

# -----------------------------------

def setup():
    '''
    Setup
    '''
    global CONF, CLIENT_MQTT, SENSORE, MOTORI, LED, RELAY
    
    util.Logger.log('setup iniziato')
    
    # Azzeramento tutti i GPIO
    for i in range(26):
        pin = machine.Pin(i, machine.Pin.OUT)
        pin.low()
    
    util.setup_led('LED')
    
    try:
        # Lettura dati dai file    
        CONF = jmng.config_load('config.json')
    
    except Exception as e:
        # Visualizzazzione dell'errore
        print(e)
        util.errore_led(9)
    
    # Allocare motori, sensori, relays
    
    RELAY = Relay(CONF.info.relays[0]['pin']['S'], CONF.info.relays[1]['pin']['S'], CONF.info.relays[2]['pin']['S'])
    SENSORE = Ky032(CONF.info.sensori[0]['pin']['S'], on_rilevazione)
    
    LED = {
            'ON': Led(CONF.info.led[0]['pin']['S']),
            'OFF': Led(CONF.info.led[1]['pin']['S'])
        }
    
    MOTORI = {
            'C-DX': Motor(CONF.info.motori[0]['pin']['inA'], CONF.info.motori[0]['pin']['inB'], CONF.info.motori[0]['pin']['en']),
            'C-SX': Motor(CONF.info.motori[1]['pin']['inA'], CONF.info.motori[1]['pin']['inB'], CONF.info.motori[1]['pin']['en']),
            'Pistoni': Motor(CONF.info.motori[2]['pin']['inA'], CONF.info.motori[2]['pin']['inB'], CONF.info.motori[2]['pin']['en']),
            'Scarico': Motor(CONF.info.motori[3]['pin']['inA'], CONF.info.motori[3]['pin']['inB'], CONF.info.motori[3]['pin']['en']),
            'Scava': Motor(CONF.info.motori[4]['pin']['inA'], CONF.info.motori[4]['pin']['inB'], CONF.info.motori[4]['pin']['en']),
            'Nastro': Motor(CONF.info.motori[5]['pin']['inA'], CONF.info.motori[5]['pin']['inB'], CONF.info.motori   [5]['pin']['en'])
        }
    
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
    
    spegni_lego()
    util.Logger.log('setup finito')

def main():
    '''
    Main dello script
    '''
    global n_pale
    setup()
    
    accendi_lego()

    
    delay = .05
    tick_per_invio = int(CONF.device['t-invio']*60 / delay)
    tick = 0
    q_tot = 0
    seriale_msg = 0
    
    while True:
        CLIENT_MQTT.check_msg()
        
        # Rilevazione sensore
        SENSORE.check()
        
        if (status or n_pale > 0) and tick == tick_per_invio:
            q = n_pale * CONF.device['q-pala']
            q_tot += q
            seriale_msg += 1
            
            msg = jmng.prepare_out_json(q, q_tot, seriale_msg, CONF.device['id'], CONF.device['tipo'],  CONF.device['descrizione'], util.Config_schema.get_struttura_dict(CONF))
            msg_c = cripta.criptazione(msg, CONF.device['k-chiave'])
            
            CLIENT_MQTT.publish(CONF.mqtt['topic_misure'], msg_c, qos=0)
            util.Logger.log(f'Inviato su {CONF.mqtt['topic_misure']}:\n{msg}')
            
            tick = 0
            n_pale = 0
            
        tick += 1
        time.sleep(delay)

try:
    if __name__ == '__main__':
        main()

except Exception as e:
    if CLIENT_MQTT:
        CLIENT_MQTT.disconnect()
    
    if RELAY:
        spegni_lego()
    
    util.Logger.log(f'Errore:\n{e}')
    util.errore_led(-1)