import psycopg2

# Conectar a la base de datos
conn = psycopg2.connect(
   host="localhost",
    database="postgres",
    user="postgres"
)

# Crear un cursor
cur = conn.cursor()

id = int(input("id : "))
# Eliminar un registro
cur.execute(f"DELETE FROM usuarios.persona WHERE id= {id}")

# Confirmar la eliminación
conn.commit()

# Cerrar la conexión
conn.close()