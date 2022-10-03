import struct
import sys
import time
from reloj import Reloj

class Cliente:
	def __init__(self, conexion):
		self.reloj = Reloj(False)
		self.conexion = conexion
		print(f"Error inicial (ms): {self.reloj.obtener_error()}")
		self.diferencias = []
		self.saludar_servidor()
		self.esperando_servidor()

	def saludar_servidor(self):
		self.conexion.enviar_mensaje(b'#')

	def esperando_servidor(self):
		while True:
			print()
			print(f"Hora: {self.reloj.obtener_reloj()}")
			print(f"Fecha: {self.reloj.obtener_fecha()}")
			print()

			_tiempo_inicial = self.reloj.obtener_reloj()
			#print(f"Tiempo inicial {_tiempo_inicial}")
			
			self.conexion.enviar_mensaje(b'@')
			_datos, _ = self.conexion.recibir_mensaje()
			_timepo_final = self.reloj.obtener_reloj()
			#print(f"Tiempo final {_timepo_final}")
			
			_t_round = _timepo_final - _tiempo_inicial
			#print(f"Latencia {_t_round}")

			try:
				datos = struct.unpack('d', _datos)[0]
				#datos_1 = time.ctime((datos)/1000)
				#print(f"Reloj del servidor {datos_1}")
				
				t_act = datos + (_t_round/2)
				#t_act_1 = time.ctime((t_act)/1000)
				#print(f"Tiempo correcto {t_act_1}")

				ajuste = self.reloj.obtener_diferencia(t_act)
				#print(f"Ajuste {ajuste}")

				self.reloj.ajustar(ajuste)

			except (struct.error, ValueError):
				simbolo, datos = struct.unpack('cd', _datos)
			time.sleep(5)

	def __del__(self):
		print(f"Saliendo...")