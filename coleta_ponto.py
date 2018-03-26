# -*- coding: UTF-8 -*-
import sys
import re
from datetime import datetime
import comunica_ponto as comunica
import gera_arquivos as arquivo
import DB
import obter_equipamento as equipamento

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

def coletar(nome_arquivo, nome_ponto):
	db = DB.DB()
	matricula = ''
	registro = ''
	inseriu_dados = False
	with open("ultima_coleta.txt", "r") as file:
		ultima_data = file.readline()

	if (nome_ponto == "SMSI"):
		nome_arquivo = 'rep_00004002050013071.txt'
		data_atual = datetime.now()
		data_final_coleta = data_atual.strftime('%d/%m/%y')
		hora_final_coleta = '%s:%02d' % (data_atual.hour, data_atual.minute)
		hora_final_coleta = '23:59'
		comunica.comunica_ponto(ultima_data_coleta('data'), '00:00', data_final_coleta, hora_final_coleta)
		print 'Comunicação executada com sucesso!'

	if (nome_arquivo != ''):
		arquivo.gera_arquivo(nome_arquivo,nome_ponto)
		print 'Arquivo registro gerado com sucesso!'
		
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
					matricula = re.search('(\d{20})', item[0])
					registro = re.search('(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})', item[0])
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
	
if __name__ == '__main__':
	nome_arquivo = sys.argv[1]
	nome_ponto = sys.argv[2].upper()
	coletar(nome_arquivo, nome_ponto)
