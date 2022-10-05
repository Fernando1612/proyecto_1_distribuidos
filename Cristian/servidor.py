import struct
import sys
import time
import threading
from reloj import Reloj

class Servidor:
	def __init__(self, conexion):
		self.reloj = Reloj(True)
		self.conexion = conexion
		print(f"Error inicial (ms): {self.reloj.obtener_error()}")
		self.conexion.bind()
		self.clientes = {}
		self._t = threading.Thread(target=self.conectar_clientes)
		self._t.start()


	def broadcast_reloj(self):
		""" Mandar mensae de roloj a los clientes"""
		print()
		print(f"Hora: {self.reloj.obtener_reloj()}")
		print(f"Fecha: {self.reloj.obtener_fecha()}")
		print()
		print("------------------")
		print("Broadcasting...")
		for dire, _ in self.clientes.items():
			_datos = bytearray(struct.pack("d",self.reloj.obtener_reloj()))
			self.conexion.enviar_mensaje(_datos, destino=dire)

	def conectar_clientes(self):
		while len(self.clientes) <= 10:
			_datos, dire = self.conexion.recibir_mensaje()
			if _datos == b'#':
				print()
				print("********************")
				print(f"Nuevo cliente {dire}")
				print("********************")
				self.clientes[dire] = 0
			elif _datos == b'@':
				self.broadcast_reloj()
			else:
				datos = struct.unpack('d', _datos)[0]
				self.clientes[dire] = datos
		print("No se permiten mas conexiones")


	def __del__(self):
		self._t.join()
		print("Saliendo")
