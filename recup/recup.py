import paho.mqtt.client as mqtt
import csv
from datetime import datetime

# Topics à écouter
TOPICS = [("IUT/Colmar2025/SAE2.04/Maison1", 0), ("IUT/Colmar2025/SAE2.04/Maison2", 0)]
CSV_FILE = "donnees_capteur.csv"

# Callback appelé quand un message est reçu
def on_message(client, userdata, msg):
    message = msg.payload.decode("utf-8")
    print(f"Reçu : {message}")
   
    # Ajoute date/heure d'enregistrement
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   
    # Enregistrement CSV
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([now, msg.topic, message])

# Configuration du client MQTT
client = mqtt.Client()
client.on_message = on_message
client.connect("test.mosquitto.org", 1883, 60)
client.subscribe(TOPICS)

# Boucle de traitement
client.loop_forever()
