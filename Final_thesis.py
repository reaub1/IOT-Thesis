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

def turn_on_LEDS():
    global current, r, g, b
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
    <html>
        <head>
            <title>ESP32 LED Control</title>
        </head>
        <body>
            <h1>Control LED Strip</h1>
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
    set_volume(volume * 327)  # Convertir le volume de 0-100 à 0-32768
    playsong(melody[song_id])  # Jouer la mélodie correspondante
    return f'Playing song: {song_id} at volume: {volume}'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)