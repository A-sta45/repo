import psycopg2

# Conectar a la base de datos
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    #password="mi_contraseña"
)
# Crear un cursor
lastname = input("apellido : ")
id = int(input("id : "))

cur = conn.cursor()
cur.execute( f"UPDATE usuarios.persona SET apellido = '{lastname}' WHERE id={id}")

# Confirmar la eliminación
conn.commit()

cur.execute( f"SELECT * FROM usuarios.persona WHERE id={id}")

# Obtener los resultados
resultados = cur.fetchall()

# Mostrar los resultados
for resultado in resultados:
    print(resultado)

# Cerrar la conexión
conn.close()