import sys
from conexion import Conexion
from servidor import Servidor
from cliente import Cliente

host = "127.0.0.1"
puerto = 1234
s = True if sys.argv[1] == "s" else False

conexion = Conexion(host, puerto)

if s:
	servidor = Servidor(conexion)
else:
	cliente = Cliente(conexion)