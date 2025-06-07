from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mqtt import Mqtt
import pymongo
from datetime import datetime
import threading
import time
import json
from movimenti import IDs
import cripta
import datetime # Importa datetime anche qui per datetime.now()

app = Flask(__name__) # Usare __app.name__ per una migliore pratica

with open('config.json','r') as f:
    config = json.load(f)

# --- Configurazione MQTT con Flask-MQTT ---
app.config['MQTT_BROKER_URL'] = config['mqtt']['broker']
app.config['MQTT_BROKER_PORT'] = config['mqtt']['porta']
app.config['MQTT_KEEPALIVE'] = config['mqtt']['keepalive']

print()
print(app.config['MQTT_BROKER_URL'])
print(app.config['MQTT_BROKER_PORT'])
print(app.config['MQTT_KEEPALIVE'])
print()

mqtt = Mqtt()

MQTT_TOPIC_COMANDI = config['mqtt']['topic_comandi']
MQTT_TOPIC_MISURE = config['mqtt']['topic_misure'] # Topic che include solo le misure
HOSTNAME = config['server']['hostname']
PORTA = config['server']['porta']
CHIAVE = config['device']['k-chiave'] # Assicurati che CHIAVE sia una stringa di byte se cripta lo richiede

with open('config_db.json','r') as f:
    db_config = json.load(f)
# --- Configurazione MongoDB ---
MONGO_URI = db_config["uri"]
MONGO_DB_NAME = db_config["database"]
MONGO_COLLECTION_NAME = db_config["collezione_misure"]
MONGO_COLLECTION_ID = db_config["collezione_id"]

try:
    mongo_client = pymongo.MongoClient(MONGO_URI)
    db = mongo_client[MONGO_DB_NAME]
    collection = db[MONGO_COLLECTION_NAME]
    print("Connesso a MongoDB!")
except pymongo.errors.ConnectionFailure as e:
    print(f"Errore di connessione a MongoDB: {e}")
    # Considera una gestione degli errori più robusta qui

# --- Variabili di stato per la dashboard ---
current_dug_quantity = 0 # Quantità scavata aggiornata via MQTT
mqtt_connected = False # Stato della connessione al broker MQTT

# --- Callbacks MQTT con Flask-MQTT ---
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    global mqtt_connected
    if rc == 0:
        print("Connesso al broker MQTT con Flask-MQTT!")
        mqtt_connected = True
        # Iscrizione al topic che ora include solo le misure
        mqtt.subscribe(MQTT_TOPIC_MISURE)
    else:
        print(f"Connessione al broker MQTT fallita con codice {rc}")
        mqtt_connected = False

@mqtt.on_disconnect()
def handle_disconnect(client, userdata, rc):
    global mqtt_connected
    print(f"Disconnesso dal broker MQTT con codice: {rc}")
    mqtt_connected = False

@mqtt.on_message()
def handle_message(client, userdata, msg):
    global current_dug_quantity
    topic = msg.topic
    payload_cifrato = msg.payload.decode('utf-8')

    if topic == MQTT_TOPIC_MISURE:
        try:
            payload_decriptato_str = cripta.decriptazione(payload_cifrato, CHIAVE)
            payload_decriptato = json.loads(payload_decriptato_str)

            print(f"Ricevuto messaggio: Topic '{topic}', Payload cifrato '{payload_decriptato_str}'")

            # Estrazione della quantità scavata dal JSON
            # Assumiamo che la quantità sia sotto 'quantita_scavata' nel payload del JSON
            current_dug_quantity = payload_decriptato['payload']['quantita']

        except (json.JSONDecodeError, ValueError, TypeError) as e:
            print(f"Errore nel processare il messaggio JSON/decriptazione: {e}")
        except Exception as e:
            print(f"Errore generico in handle_message: {e}")


# --- Funzioni di controllo del Robot (inviano JSON) ---

# Funzione ausiliaria per pubblicare comandi in JSON
def publish_command(cmd):
    global CHIAVE
    if not mqtt_connected:
        print(f"Errore: Connessione MQTT non attiva, non posso inviare comando '{cmd}'")
        return False
    msg_json = {
            "tipo": "comando",
            "payload": {
                "azione": cmd,
                "timestamp": datetime.datetime.now().isoformat()
            },
            "sender": {
                "nome": "iotp",
                "info": {}
            }
        }

    payload = json.dumps(msg_json)
    payload_c = cripta.criptazione(payload,CHIAVE)

    mqtt.publish(MQTT_TOPIC_COMANDI, payload_c)
    print(f"Comando '{cmd}' inviato a '{MQTT_TOPIC_COMANDI}' con payload cifrato.")
    return True

# Movimento Base
@app.route('/move_forward', methods=['POST'])
def move_forward():
    publish_command(IDs.Cingoli.AVANTI)
    return redirect('/')

@app.route('/move_backward', methods=['POST'])
def move_backward():
    publish_command(IDs.Cingoli.INDIETRO)
    return redirect('/')

@app.route('/turn_left', methods=['POST'])
def turn_left():
    publish_command(IDs.Cingoli.SINISTRA)
    return redirect('/')

@app.route('/turn_right', methods=['POST'])
def turn_right():
    publish_command(IDs.Cingoli.DESTRA)
    return redirect('/')

@app.route('/stop_movement', methods=['POST'])
def stop_movement():
    publish_command(IDs.Cingoli.STOP)
    return redirect('/')

# Pistoni
@app.route('/pistons_up', methods=['POST'])
def pistons_up():
    publish_command(IDs.Pistoni.SU)
    return redirect('/')

@app.route('/pistons_down', methods=['POST'])
def pistons_down():
    publish_command(IDs.Pistoni.GIU)
    return redirect('/')

@app.route('/stop_pistons', methods=['POST'])
def stop_pistons():
    publish_command(IDs.Pistoni.STOP)
    return redirect('/')

# Ruota che scava
@app.route('/digger_wheel_on', methods=['POST'])
def digger_wheel_on():
    publish_command(IDs.Scava.START)
    return redirect('/')

@app.route('/digger_wheel_off', methods=['POST'])
def digger_wheel_off():
    publish_command(IDs.Scava.STOP)
    return redirect('/')

# Scarico
@app.route('/discharge_rotate_right', methods=['POST'])
def discharge_rotate_right():
    publish_command(IDs.Scarico.DESTRA)
    return redirect('/')

@app.route('/discharge_rotate_left', methods=['POST'])
def discharge_rotate_left():
    publish_command(IDs.Scarico.SINISTRA)
    return redirect('/')

@app.route('/stop_discharge_rotation', methods=['POST'])
def stop_discharge_rotation():
    publish_command(IDs.Scarico.STOP)
    return redirect('/')

# Accensione/Spegnimento Lego
@app.route('/lego_power_on', methods=['POST'])
def lego_power_on():
    publish_command(IDs.Lego.ON)
    return redirect('/')

@app.route('/lego_power_off', methods=['POST'])
def lego_power_off():
    publish_command(IDs.Lego.OFF)
    return redirect('/')

# --- Funzioni per la quantità scavata e MongoDB ---

# Archiviazione della misura è gestita dal Raspberry, quindi non c'è una rotta '/save_dug_quantity' qui

@app.route('/get_dug_history', methods=['POST', 'GET'])
def get_dug_history():
    global current_dug_quantity
    try:
        history = list(collection.find().sort("timestamp", pymongo.DESCENDING).limit(20))
        formatted_history = []
        for entry in history:
            timestamp_obj = entry['payload']['timestamp']
            
            formatted_history.append({
                "quantity": entry['payload']['quantita'],
                "timestamp": datetime.datetime.fromtimestamp(timestamp_obj).strftime("%d/%m/%Y %H:%M:%S")
            })

        print(f'\n{history}\n')
        print(f'\n{formatted_history}\n')

        return jsonify(formatted_history)
    except Exception as e:
        print(f"Errore durante il recupero dello storico da MongoDB: {e}")
        return jsonify({"error": "Impossibile recuperare lo storico"}), 500

@app.route('/get_dashboard_status')
def get_dashboard_status():
    # Questa rotta fornisce solo la quantità scavata aggiornata e lo stato MQTT
    return jsonify({
        'current_dug_quantity': current_dug_quantity,
        'mqtt_connected': mqtt_connected
    })

# --- Pagina principale della Dashboard ---
@app.route('/')
def index():
    return render_template('dash.html',
                           mqtt_connected=mqtt_connected,
                           current_dug_quantity=current_dug_quantity)

if __name__ == '__main__':
    mqtt.init_app(app)
    app.run(HOSTNAME, PORTA, debug=True)