import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'viserver.settings'
import paho.mqtt.client as mqtt #import the client1
import ssl
import string
import random
from time import sleep

sleep(10)

def on_message_ping(clientPing, userdata, message):
    authentication_classes=[]
    permission_classes=[]
    message = str(message.payload.decode("utf-8"))
    print(message)
    #had to write manual command handling here
    if message == "h":
        print ("hello")

def on_connect(client, userdata, flags, rc):
    print("connected")
    client.subscribe("newvisiontopic1")

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)

module_dir= os.path.dirname(__file__)
TLS_CERT_PATH=os.path.join(module_dir,'newvision_root.cer')
broker_address="************"
clientPing = mqtt.Client(get_random_string(8)) #create new instance
clientPing.username_pw_set(username="*****",password="*****")
clientPing.on_connect = on_connect
clientPing.on_message=on_message_ping #attach function to callback
print("connecting to broker...")
clientPing.tls_set(ca_certs=TLS_CERT_PATH, certfile=None,keyfile=None, cert_reqs=ssl.CERT_REQUIRED,tls_version=ssl.PROTOCOL_TLS, ciphers=None)
clientPing.tls_insecure_set(False)
clientPing.connect(broker_address,port=8883) #connect to broker
clientPing.loop_start()
#clientPing.loop_forever()
