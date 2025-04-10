import sys
sys.path.append("/music")
from music.play import playsong, melody, set_volume
from microdot import Microdot, Response
import network


Name = "ESP32 Wifi ROBIN"
Password = "123456789"

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=Name, password=Password, authmode=3)

while not ap.active():
    print("creating")
    time.sleep(0.5)

print(ap.ifconfig())

app = Microdot()
Response.default_content_type = 'text/html'

@app.route('/')
def index(request):
    try:
        with open('index.html', 'r') as file:
            html_content = file.read()
        return html_content
    except OSError as e:
        return f"Error reading file: {e}", 500

@app.route('/play_song', methods=['POST'])
def play_song(request):
    song_id = int(request.form['song'])
    set_volume(32768//128)
    playsong(melody[song_id])
    return 'Playing song ID: {}'.format(song_id)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
