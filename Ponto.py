class Ponto:
	""" Classe que represenda o relogio ponto com local, numero do codigo no banco de dados e numero do aparelho """
	def __init__(self, local, numero, rep=None):
		self.local = local
		self.numero = numero
		self.rep = rep
	
	def get_local(self):
		return self.local

	def get_numero(self):
		return self.numero
	
	def get_rep(self):
		return self.rep