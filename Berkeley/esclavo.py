import struct
import sys
from reloj import Reloj

class Esclavo:
	def __init__(self, conexion):
		self.reloj = Reloj()
		self.conexion = conexion
		print(f"Error inicial (ms): {self.reloj.obtener_error()}")
		self.diferencias = []
		self.saludar_maestro()
		self.esperando_maestro()

	def saludar_maestro(self):
		self.conexion.enviar_mensaje(b'#')

	def esperando_maestro(self):
		while True:
			print()
			print(f"Hora: {self.reloj.obtener_reloj()}")
			print(f"Fecha: {self.reloj.obtener_fecha()}")
			print()

			_datos, _ = self.conexion.recibir_mensaje()

			try:
				datos = struct.unpack('d', _datos)[0]
			except (struct.error, ValueError):
				simbolo, datos = struct.unpack('cd', _datos)
			if simbolo == b'@':
				self.reloj.ajustar(datos)
				simbolo = ''
			else:
				self.enviar_diferencia(datos)
				print("----------------------")

	def enviar_diferencia(self, datos):
		diferencia = self.reloj.obtener_diferencia(datos)
		_diferencia = bytearray(struct.pack('d', diferencia))
		self.conexion.enviar_mensaje(_diferencia)
		print(f'Diferencia (ms) {diferencia}')
		self.diferencias.append(diferencia)

	def promedio_diferencias(self):
		suma = 0.0
		for diferencia in self.diferencias[1:]:
			suma += diferencia

		try:
			return suma / len(self.diferencias)
		except ZeroDivisionError:
			return 0.0
		

	def __del__(self):
		print(f"Diferencia media: {self.promedio_diferencias()}")