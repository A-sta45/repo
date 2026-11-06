# Repo — Proyectos varios

Colección de pequeños proyectos y ejercicios independientes.

## Contenido

- **`adminostradorT/`** — script en **MicroPython** para controlar un LED WS2812 (NeoPixel) desde el teclado: cada tecla cambia el color (`r`=rojo, `g`=verde, `b`=azul, `y`=amarillo, `w`=blanco, `o`=apagado). Pensado para correr en un microcontrolador (ESP32/RP2040).
- **`automatas/`** — editor gráfico de autómatas finitos hecho con **Tkinter**: permite crear y arrastrar estados en un canvas, marcar estados iniciales/finales y dibujar transiciones.
- **`BaseDeDatos/`** — scripts de ejemplo para CRUD sobre **PostgreSQL** (`main.py`, `base_1.py`, `update.py`, `delite.py`) y un `docker-compose.yml` para levantar Postgres localmente.
- **`crud/`** — ejemplo de panel de administración con **FastAPI/Starlette**, `SQLModel` y `starlette-admin` sobre una tabla `Todo`.
- **`dibujo/`** y **`dibujo.py`** — scripts con `matplotlib`/`numpy` que generan figuras (ej. `coliflor.py` dibuja un patrón fractal tipo espiral de Fibonacci, `ruleta.py` dibuja una ruleta).
- **`lector_analogo/`** — servicio con **FastAPI** que lee un sensor analógico por puerto serial y expone los últimos valores vía API (con CORS habilitado).
- **`ProyectoAutomata/`** — versión en **Java** (Swing/AWT) de un editor de autómatas finitos.
- **`prueba_java/`** — archivo de pruebas.

## Notas

- Cada subcarpeta es independiente: revisa el código de cada una para ver sus dependencias puntuales (por ejemplo `BaseDeDatos` y `crud` necesitan PostgreSQL; `adminostradorT` necesita un microcontrolador con MicroPython; `lector_analogo` necesita un puerto serial disponible).
- `BaseDeDatos` incluye `docker-compose.yml` para levantar Postgres rápido:
  ```bash
  cd BaseDeDatos
  docker compose up -d
  ```
