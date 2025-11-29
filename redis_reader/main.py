from machine import Pin
from neopixel import NeoPixel
from redis import Redis
import time

#Configure the built-in WS2812 LED pins of RP2040-ETH and set the number of LEDs to 1
strip = NeoPixel(Pin(25), 1)
strip[0] = ( 255,0,0)
strip.write()


# --- Example Redis PING test ---
r = Redis()

# --- Main loop ---
while True:
    print( r.keys() )
    time.sleep(2)