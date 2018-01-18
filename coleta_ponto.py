# -*- coding: UTF-8 -*-
import firebirdsql as data_base
import comunica_ponto as comunica
import gera_arquivos as arquivo
import re
from datetime import datetime
import time
import sys

conexao = data_base.connect(dsn='192.168.50.6:/home/henry/Henry.fdb', user='SYSDBA', password='masterkey')

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

def verifica_exite(matricula, registro):
	sql = "SELECT * FROM HE22 WHERE HE22_ST_MATRICULA = '%s' AND HE22_DT_REGISTRO = '%s'" % (matricula, registro)
	cursor = conexao.cursor()
	cursor.execute(sql)
	resultado = cursor.fetchone()
	cursor.close()
	existe = resultado != None
	#if(existe):
	#	print 'Não serei inserido!'
	return existe

def insere_dado(sql):
	inserir = conexao.cursor()
	inserir.execute(sql)
	conexao.commit()
	inserir.close()
	#print 'Dado inserido com sucesso!'

def atualiza_ultima_coleta(inseriu_dados, data, hora):
	if (inseriu_dados):
		with open("ultima_coleta.txt", "w") as ultima_coleta:
			ultima_coleta.write("%s %s" % (data, hora))
			print 'Ultima data atualizada com sucesso!'

def coletar(nome_arquivo, nome_ponto):
	count_inserts = 0
	count_not_inserts = 0

	inseriu_dados = False
	with open("ultima_coleta.txt", "r") as file:
		ultima_data = file.readline()

	data_atual = datetime.now()

	data_final_coleta = data_atual.strftime('%d/%m/%y')
	hora_final_coleta = '%s:%02d' % (data_atual.hour, data_atual.minute)
	hora_final_coleta = '23:59'
	comunica.comunica_ponto(ultima_data_coleta('data'), '00:00', data_final_coleta, hora_final_coleta)
	#time.sleep(30)
	print 'Comunicação executada com sucesso!'
	if (nome_arquivo != ''):
		arquivo.gera_arquivo(nome_arquivo,nome_ponto)
		print 'Arquivo registro gerado com sucesso!'
		
		arquivo.filtrar(nome_ponto)
		print 'Arquivo filtrado para ter somente o mes atual e o anterior!'
	
	arquivo.gera_insert_de_registro_txt(nome_ponto)
	#time.sleep(10)
	print 'Arquivo inserte gerado com sucesso!'
	
	
	with open('dbInsertRegistro.txt', 'r') as arq_db:
		print('Inserindo registros no banco de dados.')
		lista = []
		count = 0
		for linha in arq_db:
			lista.append(re.split(r'\n', linha))
		
		tamanho_lista = len(lista)
		print "%d a serem verificados e inseridos" % tamanho_lista
		for item in lista:
			count += 1
			if (item != ''):
				matricula = re.search('(\d{20})', item[0])
				registro = re.search('(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})', item[0])
				if(not verifica_exite(matricula.group(1), registro.group(1))):
					sql = item
					insere_dado(sql[0])
					inseriu_dados = True
					count_inserts+=1
				else:
					count_not_inserts+=1

				current_percentual = float(count*100)/float(tamanho_lista)
				print("{:.1f}% .................................. de {}/{}".format(current_percentual, count,tamanho_lista))
					
		print "Foram inserido(s) %d registro(s)" % count_inserts
		print "Registro(s) %d que ja exitem no banco de dados e não foram inseridos" % count_not_inserts

	atualiza_ultima_coleta(inseriu_dados, data_final_coleta, hora_final_coleta)
	
if __name__ == '__main__':
	nome_arquivo = sys.argv[1]
	nome_ponto = sys.argv[2].upper()
	coletar(nome_arquivo, nome_ponto)
