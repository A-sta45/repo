from typing import Union
from fastapi import FastAPI
import psycopg2


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/base_de_datos")
def read_bd():
    # Conectar a la base de datos
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
    )
    # Crear un cursor
    cur = conn.cursor()

    # Ejecutar una consulta SQL
    cur.execute("SELECT * FROM usuarios.persona ORDER BY nombre DESC")

    # Obtener los resultados
    resultados = cur.fetchall()

    # Obtener los nombres de las columnas
    column_names = [desc[0] for desc in cur.description]

    # Convertir los resultados en una lista de diccionarios
    lista_de_datos = []
    for resultado in resultados:
        resultado_dict = dict(zip(column_names, resultado))
        lista_de_datos.append(resultado_dict)

    # Cerrar la conexión
    conn.close()

    return {"datos": lista_de_datos}


@app.get("/base_de_datos/{id}")
def read_one_item(id: int):
    # Conectar a la base de datos
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
    )
    # Crear un cursor
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM usuarios.persona WHERE id={id}")

    # Obtener los resultados
    resultados = cur.fetchall()

    # Obtener los nombres de las columnas
    column_names = [desc[0] for desc in cur.description]

    # Convertir los resultados en una lista de diccionarios
    lista_de_datos = []
    for resultado in resultados:
        resultado_dict = dict(zip(column_names, resultado))
        lista_de_datos.append(resultado_dict)

    # Cerrar la conexión
    conn.close()

    return {"datos": lista_de_datos}


@app.post("/base_de_datos")
def crate_one_item(name: str, lastname: str, age: int):
    # Conectar a la base de datos
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        # password="mi_contraseña"
    )

    # Crear un cursor
    cur = conn.cursor()

    # Ejecutar una consulta SQL
    cur.execute(
        f"INSERT INTO usuarios.persona (nombre, apellido, edad) VALUES ('{name}', '{lastname}', {age})")

    # Obtener el ID del registro recién insertado
    new_id = cur.fetchone()[0]

    # Confirmar la transacción
    conn.commit()

    # Ejecutar una consulta SQL
    cur.execute(f"SELECT * FROM usuarios.persona WHERE id={new_id}")

    # Obtener los resultados
    resultados = cur.fetchall()

    # Obtener los nombres de las columnas
    column_names = [desc[0] for desc in cur.description]

    # Convertir los resultados en una lista de diccionarios
    lista_de_datos = []
    for resultado in resultados:
        resultado_dict = dict(zip(column_names, resultado))
        lista_de_datos.append(resultado_dict)

    return {"datos": lista_de_datos}
