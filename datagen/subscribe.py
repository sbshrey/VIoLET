import paho.mqtt.client as mqtt
from time import time, sleep
import uuid
import sys


INTERVAL = 1
QOS = 0
msg="ON"
topic1="pub"
topic2="sub"

#def on_connect(client, userdata, flags, rc):
#    print("connected")
#    #global topic1
#    #client.subscribe(topic1)
#    #client.publish(topic2, time(), qos=QOS)


def on_message(client, userdata, message):
    global topic2
    global msg
    msg = message.payload.decode('utf-8')
    print(msg)
    print(topic2)
    client.publish(topic2, msg)   

    


def main(argv):
    global topic1
    global topic2
    sensor_id=argv[1]
    host=argv[2]
    port=1883
    #rtt_array = []
    topic1 = "pub_"+sensor_id
    topic2 = "sub_"+sensor_id
    client = mqtt.Client()
    #client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host,port)
    client.subscribe(topic1)
    client.loop_forever()


if __name__=="__main__":
    main(sys.argv)
