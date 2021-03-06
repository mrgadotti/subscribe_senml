import paho.mqtt.client as mqtt
import sys
import json
from datetime import datetime

host = "mqtt.eclipse.org"
port = 1883
keep_alive = 60
topic = "faustao/#"  

def on_connect(client, userdata, flags, rc):
    print("[STATUS] Conected: " + str(rc))
    client.subscribe(topic)


def on_message(client, userdata, msg):
    received_var = str(msg.payload, "utf-8")
    # print(msg.topic + " > " + str(msg.payload,'utf-8'))
    #print(f"[MESSAGE] {received_var}")
    print_senml(received_var)


def print_senml(msg):
    json_data = json.loads(msg)
    #print (json_data)
    try:
        read_timestamp = int(json_data[0]["bt"] / 1000000)
        dt_object = datetime.fromtimestamp(read_timestamp)
        dt_read_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')

        print(
            f'[MESSAGE]'
            f' MAC: {json_data[0]["bn"]} Time: {dt_read_time}' 
            f' Model: {json_data[1]["vs"]} Name: {json_data[2]["n"]}'
            f' Value: {json_data[2]["v"]} {json_data[2]["u"]}'
        )
    except:
        print(
            f'[MESSAGE]'
            f' MAC: {json_data[0]["bn"]} Time: {dt_read_time}' 
            f' Model: {json_data[1]["vs"]} Name: {json_data[2]["n"]}'
            f' Value: {json_data[2]["vb"]}'
        )
        pass

def main():
    try:
        print("[STATUS] Init MQTT...")
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(host, port, keep_alive)
        client.loop_forever()

    except KeyboardInterrupt:
        print("\n[STATUS] Exiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
