from machine import Pin, PWM
from utime import sleep

from music.melodies import *
from music.notes import *

buzzer = PWM(Pin(14), freq=30000)
volume = 0

def playtone(frequency):
    buzzer.duty_u16(volume)
    buzzer.freq(frequency)


def be_quiet():
    buzzer.duty_u16(0)

def duration(tempo, t):
    wholenote = (60000 / tempo) * 4
    
    if t > 0:
        noteDuration = wholenote // t
    elif (t < 0):
        noteDuration = wholenote // abs(t)
        noteDuration *= 1.5
    return noteDuration


def playsong(mysong):
    try:
        print(mysong[0])
        tempo = mysong[1]
        
        for thisNote in range(2, len(mysong), 2):

            noteduration = duration(tempo, int(mysong[thisNote + 1]))

            if (mysong[thisNote] == "REST"):
                be_quiet()
            else:
                playtone(notes[mysong[thisNote]])

            sleep(noteduration * 0.9 / 1000)
            be_quiet()
            sleep(noteduration * 0.1 / 1000)

    except:
        be_quiet()

def set_volume(new_volume):
    """Set the volume of the music."""
    global volume
    volume = new_volume
