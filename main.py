from microdot import Microdot, Response
import network
import time
from neopixel import NeoPixel
from machine import Pin,I2C
import ssd1306

import sys
sys.path.append("/music")

i2c = I2C(0, scl = Pin(22) , sda = Pin(21), freq = 400000)

oled = ssd1306.SSD1306_I2C(128, 32, i2c)

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

import time

import time

def turn_on_LEDS(color, intensity=100, rotation_speed=0.1):
    global current
    r, g, b = color

    max_r = int((r / 100) * intensity)
    max_g = int((g / 100) * intensity)
    max_b = int((b / 100) * intensity)

    for brightness in range(0, intensity + 1, 5):
        current_r = int((max_r / intensity) * brightness)
        current_g = int((max_g / intensity) * brightness)
        current_b = int((max_b / intensity) * brightness)

        for i in range(12):
            if i < current:
                led_strip[i] = (current_r, current_g, current_b)
            else:
                led_strip[i] = (0, 0, 0)
        led_strip.write()
        time.sleep(0.05)
    for _ in range(12):
        first_led = led_strip[0]

        for i in range(11):
            led_strip[i] = led_strip[i + 1]

        led_strip[11] = first_led

        led_strip.write()
        time.sleep(rotation_speed)

    for i in range(12):
        if i < current:
            led_strip[i] = (max_r, max_g, max_b)
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
    set_volume(volume * 100)

    if song_id == 0:
        turn_on_LEDS((255, 255, 0))
        display_oled("Pacman")
    elif song_id == 1:
        turn_on_LEDS((0, 0, 255))
        display_oled("Stars Wars")
    elif song_id == 2:
        turn_on_LEDS((255, 0, 0))
        display_oled("Darth Vader")
    
    playsong(melody[song_id])

    return Response(status_code=303, headers={'Location': '/'})

def display_oled(text):
    oled.fill(0)
    oled.text(text,0,0)
    oled.show()
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
