import paho.mqtt.client as mqtt
import time
import cripta

c = None

def oc(client, userdata, flags, rc, properties):
    if rc == 0:
        print('connesso')

    c.subscribe('iiseuganeoprojects/escavatore/ruspa-1/misure')

def om(client, userdata, msg):
    print(cripta.decriptazione(msg.payload.decode('utf-8'), 'ABCD'))

c = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
c.on_connect = oc
c.on_message = om

c.connect('broker.hivemq.com', 1883, 600)

c.loop_start()

c.publish('iiseuganeoprojects/escavatore/ruspa-1/comandi', cripta.criptazione('{"aaaa": 1}', 'ABCD'), 0)

while True:
    time.sleep(0.1)

c.loop_stop()
c.disconnect()