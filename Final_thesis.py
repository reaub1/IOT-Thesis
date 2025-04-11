from microdot import Microdot, Response
import network
import time
from neopixel import NeoPixel
from machine import Pin

import sys
sys.path.append("/music")

from music.play import *

Name = "ESP32 Wifi ROBIN"
Password = "123456789"

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=Name, password=Password, authmode=3)

while not ap.active():
    print("creating")
    time.sleep(0.5)

print(ap.ifconfig())

led_strip = NeoPixel(Pin(23), 12)

current = 12
r = 0
g = 0
b = 0

def turn_on_LEDS(color):
    global current
    r, g, b = color
    for i in range(12):
        if i < current:
            led_strip[i] = (r, g, b)
        else:
            led_strip[i] = (0, 0, 0)
    led_strip.write()

app = Microdot()
Response.default_content_type = 'text/html'

@app.route('/')
def index(request):
    return '''
    <!DOCTYPE html>
<html>
<head>
    <title>ESP32 JukeBox</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            height: 100vh;
        }

        h1 {
            color: #333;
            margin-top: 20px;
        }

        form {
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 300px;
            margin-top: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
        }

        input[type="range"] {
            width: 100%;
            margin-bottom: 20px;
        }

        button {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            border: none;
            border-radius: 4px;
            background-color: #007BFF;
            color: white;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <h1>ESP32 JukeBox</h1>
    <form action="/play" method="post">
        <label for="volume">Volume:</label>
        <input type="range" id="volume" name="volume" min="0" max="100" value="100"><br><br>
        <button type="submit" name="song" value="0">Pacman</button>
        <button type="submit" name="song" value="1">Star Wars theme</button>
        <button type="submit" name="song" value="2">Darth Vader theme</button>
    </form>
</body>
</html>
    '''

@app.route('/play', methods=['POST'])
def play(request):
    song_id = int(request.form['song'])
    volume = int(request.form['volume'])
    set_volume(volume * 327)

    # Définir la couleur en fonction de la chanson
    if song_id == 0:
        turn_on_LEDS((255, 255, 0))  # Jaune pour Pacman
    elif song_id == 1:
        turn_on_LEDS((0, 0, 255))    # Bleu pour Star Wars
    elif song_id == 2:
        turn_on_LEDS((255, 0, 0))    # Rouge pour Darth Vader

    playsong(melody[song_id])

    # Rediriger vers la page d'accueil
    return Response(status_code=303, headers={'Location': '/'})

def display_information(text):
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
