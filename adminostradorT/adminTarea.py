from machine import Pin
import neopixel
import sys
import select

# ----- Configuracion WS2812 -----
NUM_LEDS = 1
np = neopixel.NeoPixel(Pin(0), NUM_LEDS)

# Funcion para cambiar color
def color(r, g, b):
    np[0] = (r, g, b)
    np.write()

print("Control WS2812")
print("r = rojo")
print("g = verde")
print("b = azul")
print("y = amarillo")
print("w = blanco")
print("o = apagar")

# Detectar teclado sin bloquear
poll = select.poll()
poll.register(sys.stdin, select.POLLIN)

while True:
    if poll.poll(10):
        tecla = sys.stdin.read(1)

        if tecla == 'r':
            color(255, 0, 0)
        elif tecla == 'g':
            color(0, 255, 0)
        elif tecla == 'b':
            color(0, 0, 255)
        elif tecla == 'y':
            color(255, 255, 0)
        elif tecla == 'w':
            color(255, 255, 255)
        elif tecla == 'o':
            color(0, 0, 0)