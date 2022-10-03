import random
import time

class Reloj:
	def __init__(self, servidor):
		self.servidor = servidor
		if servidor:
			self.error = 0
		else:
			self.error = random.randint(0, 30) * 1000.0
		self.hora_actual = lambda: time.time() * 1000.0

	def obtener_error(self):
		return self.error

	def obtener_reloj(self):
		return self.hora_actual() + self.error

	def ajustar(self, ajuste):
		self.error = ajuste

	def obtener_fecha(self):
		return time.ctime((self.obtener_reloj())/1000)

	def obtener_diferencia(self, diferencia):
		return diferencia -self.hora_actual()