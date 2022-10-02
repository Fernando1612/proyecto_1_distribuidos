import struct
import sys
import time
import threading
from reloj import Reloj

class Maestro:
	def __init__(self, conexion):
		self.reloj = Reloj()
		self.conexion = conexion
		print(f"Error inicial (ms): {self.reloj.obtener_error()}")
		self.conexion.bind()
		self.esclavos = {}
		self._t = threading.Thread(target=self.conectar_esclavos)
		self._t.start()
		self.bucle()

	def bucle(self):
		while True:
			print()
			print(f"Hora: {self.reloj.obtener_reloj()}")
			print(f"Fecha: {self.reloj.obtener_fecha()}")
			print()
			print("------------------")
			print("Broadcasting...")
			self.broadcast_reloj()
			time.sleep(10)
			self.actualizar_relojes()

	def broadcast_reloj(self):
		""" Mandar mensae de roloj a los esclavos"""
		for dire, _ in self.esclavos.items():
			_datos = bytearray(struct.pack("d",self.reloj.obtener_reloj()))
			self.conexion.enviar_mensaje(_datos, destino=dire)

	def conectar_esclavos(self):
		while len(self.esclavos) <= 10:
			_datos, dire = self.conexion.recibir_mensaje()
			if _datos == b'#':
				print("********************")
				print(f"Nuevo esclavo {dire}")
				print("********************")
				self.esclavos[dire] = 0
			else:
				datos = struct.unpack('d', _datos)[0]
				self.esclavos[dire] = datos
		print("No se permiten mas conexiones")


	def actualizar_relojes(self):
		promedio = self.calcular_promedio()
		print(f"Promedio: {promedio}")
		self.reloj.ajustar(promedio)
		for dire, diferencia in self.esclavos.items():
			ajuste = (diferencia * -1) + promedio
			print(f"Ajuste {ajuste}")
			_ajuste = bytearray(struct.pack('cd', b'@',ajuste))
			self.conexion.enviar_mensaje(_ajuste, destino=dire)


	def calcular_promedio(self):
		promedio = 0.0
		for _,diferencia in self.esclavos.items():
			promedio += diferencia
		try:
			return promedio / (len(self.esclavos)+1)
		except ZeroDivisionError:
			return 0.0

	def __del__(self):
		self._t.join()
		print("Saliendo")
