# -*- coding: UTF-8 -*-
import sys
import re
from datetime import datetime
import os.path
import comunica_ponto as comunica
import gera_arquivos as arquivo
import DB
import obter_equipamento as equipamento

def verifica_arquivo(nome_arq):
	if(os.path.isfile("AFD"+nome_arq+".txt")):
		return "AFD"+nome_arq+".txt"
	elif(os.path.isfile("REP"+nome_arq+".txt")):
		return "REP"+nome_arq+".txt"
	elif(os.path.isfile("rep_"+nome_arq+".txt")):
		return "rep_"+nome_arq+".txt"
	elif(os.path.isfile(nome_arq+".txt")):
		return nome_arq+".txt"
	else:
		return ''

def ultima_data_coleta(opc):
	with open("ultima_coleta.txt", "r") as file:
		ultima_data = file.readline()
	
	data = re.search('(\d{2})\/(\d{2})\/(\d{2})\s(\d{2}:\d{2})', ultima_data)
	
	if (opc == 'sql'):
		return '20%s-%s-%s %s' % (data.group(3), data.group(2), data.group(1), data.group(4))
	elif (opc == 'data'):
		return '%s/%s/%s' % (data.group(1), data.group(2), data.group(3))
	elif (opc == 'hora'):
		return data.group(4)


def atualiza_ultima_coleta(inseriu_dados, data, hora):
	if (inseriu_dados):
		with open("ultima_coleta.txt", "w") as ultima_coleta:
			ultima_coleta.write("%s %s" % (data, hora))

def coletar_ponto(ponto):
	nome_arquivo = ''
	db = DB.DB()
	inseriu_dados = False
	nome_ponto = ponto.get_local()

	print(nome_ponto)

	if (ponto.get_local() == "SMSI"):
		data_atual = datetime.now()
		data_final_coleta = data_atual.strftime('%d/%m/%y')
		hora_final_coleta = '%s:%02d' % (data_atual.hour, data_atual.minute)
		hora_final_coleta = '23:59'
		comunica.comunica_ponto(ultima_data_coleta('data'), '00:00', data_final_coleta, hora_final_coleta)
		print 'Comunicação executada com sucesso!'
	
	if(ponto.get_rep() != None):
		try:
			nome_arquivo = verifica_arquivo(ponto.get_rep())
		except IOError:
			raise
				
	if (nome_arquivo != ''):
		arquivo.gera_arquivo(nome_arquivo, nome_ponto)
		print 'Arquivo registro gerado com sucesso!'
		print "Lendo arquivo " + nome_arquivo
		
		print 'Filtrando e verificando no banco de dados'
		arquivo.filtrar(nome_ponto)
		print 'Arquivo filtrado e verificado no banco de dados!'
		
		arquivo.gera_insert_de_registro_txt(nome_ponto)
		print 'Arquivo para inserir no banco de dados gerado com sucesso!'
		
		
		with open('dbInsertRegistro.txt', 'r') as arq_db:
			lista = []
			count = 0
			for linha in arq_db:
				lista.append(re.split(r'\n', linha))
			
			tamanho_lista = len(lista)
			if(tamanho_lista > 0):
				print('Inserindo registros no banco de dados.')
				print "%d para serem inseridos" % tamanho_lista
				for item in lista:
					count += 1
					if (item != ''):
						#matricula = re.search('(\d{20})', item[0])
						#registro = re.search('(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})', item[0])
						sql = item
						db.inserir_registro(sql[0])
						inseriu_dados = True
						current_percentual = float(count*100)/float(tamanho_lista)
						print("{:.1f}% .................................. de {}/{}".format(current_percentual, count,tamanho_lista))

				if (nome_ponto == "SMSI"):
					atualiza_ultima_coleta(inseriu_dados, data_final_coleta, hora_final_coleta)
					print 'Ultima data atualizada com sucesso!'
			else:
				print "Não ha dados para serem inseridos"
			
			if(nome_arquivo != ''):
				os.remove(nome_arquivo)

def coletar(nome_ponto = ''):

	print nome_ponto
	
	if(nome_ponto != ''):
		ponto = equipamento.obter_equipamento(nome_ponto)
		coletar_ponto(ponto)
	else:
		pontos = []
		pontos.append(equipamento.obter_equipamento('SMSI'))
		pontos.append(equipamento.obter_equipamento('FARMACIA'))
		pontos.append(equipamento.obter_equipamento('BELA_VISTA'))
		pontos.append(equipamento.obter_equipamento('CENTRAL_REG'))
		pontos.append(equipamento.obter_equipamento('CEREST'))
		pontos.append(equipamento.obter_equipamento('GRAJAU'))
		pontos.append(equipamento.obter_equipamento('IMPERADOR'))
		pontos.append(equipamento.obter_equipamento('MARINGA'))
		pontos.append(equipamento.obter_equipamento('SAO_JORGE'))
		pontos.append(equipamento.obter_equipamento('SAMU'))
		pontos.append(equipamento.obter_equipamento('UPA'))
		pontos.append(equipamento.obter_equipamento('MARIANA'))
		pontos.append(equipamento.obter_equipamento('SAO_BENEDITO'))
		pontos.append(equipamento.obter_equipamento('SAO_MIGUEL'))
		pontos.append(equipamento.obter_equipamento('TAQUARI'))
		pontos.append(equipamento.obter_equipamento('APARECIDA'))
		pontos.append(equipamento.obter_equipamento('BOM_JESUS'))
		pontos.append(equipamento.obter_equipamento('CIMENTOLANDIA'))
		pontos.append(equipamento.obter_equipamento('MATERNO'))
		pontos.append(equipamento.obter_equipamento('CENTRO_DIA'))		
		pontos.append(equipamento.obter_equipamento('CAMARGO'))
		pontos.append(equipamento.obter_equipamento('SAO_ROQUE'))
		pontos.append(equipamento.obter_equipamento('SAO_CAMILO'))
		pontos.append(equipamento.obter_equipamento('GUARI'))
		pontos.append(equipamento.obter_equipamento('SANTA_MARIA'))
		pontos.append(equipamento.obter_equipamento('PACOVA'))
		pontos.append(equipamento.obter_equipamento('ALTO_BRANCAL'))
		pontos.append(equipamento.obter_equipamento('AGROVILA'))
		pontos.append(equipamento.obter_equipamento('CAPUTERA'))
		pontos.append(equipamento.obter_equipamento('CME'))
		pontos.append(equipamento.obter_equipamento('CS1'))
		pontos.append(equipamento.obter_equipamento('VIRGINIA'))

		for ponto in pontos:
			coletar_ponto(ponto)			
	
if __name__ == '__main__':
	try:
		nome_ponto = sys.argv[1].upper()
		coletar(nome_ponto)
	except IndexError:
		coletar()
