import socket

class Conexion:
	def __init__(self, host, puerto):
		self.destino = (host, puerto)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		
	def enviar_mensaje(self, datos, **kwargs):
		try:
			self.sock.sendto(datos, kwargs['destino'])
		except KeyError:
			self.sock.sendto(datos, self.destino)

	def recibir_mensaje(self):
		datos, direccion = self.sock.recvfrom(4096)
		return datos, direccion

	def bind(self):
		self.sock.bind(self.destino)

	def __del__(self):
		self.sock.close()