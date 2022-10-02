import sys
from conexion import Conexion
from maestro import Maestro
from esclavo import Esclavo

host = "127.0.0.1"
puerto = 1234
m = True if sys.argv[1] == "m" else False

conexion = Conexion(host, puerto)

if m:
	maestro = Maestro(conexion)
else:
	esclavo = Esclavo(conexion)