from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import serial
import threading
from collections import deque
import time

app = FastAPI()

# Configuración Serial (ajusta el puerto COM)
# serial_port = "COM3"  # Windows: COMx | Linux: /dev/ttyACM0
serial_port = "/dev/ttyACM0"  # Windows: COMx | Linux: /dev/ttyACM0
baudrate = 115200

# Buffer para almacenar los últimos 10 valores
data_buffer = deque(maxlen=10)

# Configura CORS (permite peticiones desde cualquier origen)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def leer_serial():
    with serial.Serial(serial_port, baudrate, timeout=1) as ser:
        while True:
            try:
                linea = ser.readline().decode('utf-8').strip()
                if linea:  # Si hay dato válido
                    data_buffer.append(float(linea))
            except (UnicodeDecodeError, ValueError):
                continue

# Inicia hilo para lectura serial
threading.Thread(target=leer_serial, daemon=True).start()

@app.get("/datos")
def obtener_datos():
    """Endpoint que devuelve los últimos valores recibidos"""
    return {
        "valores": list(data_buffer),
        "ultimo_valor": data_buffer[-1] if data_buffer else None,
        "timestamp": time.time()
    }
