print("hola mundo")
import psycopg2

# Conectar a la base de datos
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    #password="mi_contraseña"
)

# Crear un cursor
cur = conn.cursor()

# Ejecutar una consulta SQL
cur.execute("SELECT * FROM usuarios.persona ORDER BY nombre DESC")

# Obtener los resultados
resultados = cur.fetchall()



# Mostrar los resultados
for resultado in resultados:
    print(resultado)

# Cerrar la conexión
conn.close()