# -*- coding: iso8859-1 -*-
import re
import time
from datetime import datetime
import sys
import verifica_codigo_unidade as unidade
import DB

def clean_files(filename):
	file = open(filename, 'w')
	file.write('')
	file.close()

def registros_db(ponto, mes, ano):
	db = DB.DB()
	registros = []
	if(mes == "02"):
		if(int(mes) % 4 == 0):
			dia = "29"
		else:
			dia = "28"
	elif(mes == "01" or mes == "03" or mes == "05" or mes == "07" or mes == "08" or mes == "10" or mes == "12"):
		dia = "31"
	else:
		dia = "30"
	
	resultados = db.obter_registros_periodo(ponto, ano, mes, dia)
	
	for linha in resultados:
		data_time = str(linha[11]).split(' ')
		data = data_time[0].split('-')
		registros.append("01 N 0   %s/%s/%s %s %s" % (data[2], data[1], data[0], data_time[1], linha[2]))
	
	return registros

def lista_refatorada(codigo_ponto, filename, mes, ano, atual=False):
	lista = []
	
	if(not atual):
		if (mes == "01"):
			mes = "12"
			ano = int(ano) - 1
		else:
			mes = str(int(mes) - 1).zfill(2)	

	verifica_db(codigo_ponto, filename, mes, ano)		

	expr = '01\sN\s0\s+\d{2}\/%s\/%s\s\d{2}:\d{2}:\d{2}\s\d{20}' % (mes, ano)
	with open(filename, 'r') as arquivo:
		for linha in arquivo:
			item = re.search(expr, linha)
			if item != None:
				lista.append(item.group()+"\r\n")

	return lista

def filtrar(ponto_nome):
	filename = 'registros_{}.txt'.format(ponto_nome.lower())
	codigo_ponto = unidade.verificar_numero_ponto(ponto_nome)
	current_month = datetime.now().strftime('%m')
	current_year = datetime.now().strftime('%Y')
	anterior = lista_refatorada(codigo_ponto, filename, current_month, current_year)
	atual = lista_refatorada(codigo_ponto, filename, current_month, current_year, True)

	clean_files(filename)

	with open(filename, 'a') as arquivo:
		for item in anterior:
			arquivo.write(item)

	with open(filename, 'a') as arquivo:
		for item in atual:
			arquivo.write(item)
	

def verifica_db(codigo_ponto, filename, mes, ano):
	dados_arq = []
	dados_db = registros_db(codigo_ponto, mes, ano)

	with open(filename, 'r') as arquivo:
		for dado in arquivo:
			dados_arq.append(dado)
	
	clean_files(filename)
	
	with open(filename, 'a') as arquivo:
		for dado in dados_db:
			count = 0
			for linha in dados_arq:
				result = re.search(dado, linha)
				if(result != None):
					dados_arq.pop(count)
					break
				count += 1
		
		for linha in dados_arq:
			if(len(dados_arq) > 0):
				arquivo.write(linha)
			

def monta_insert(colaborado_matricula, data_registro, numero_ponto):
	insert = "INSERT INTO HE22 VALUES(NULL,'%s','%s','0','0','0','2','0','4','255','1','%s','0','0','4','0','0');\n" % (numero_ponto,colaborado_matricula, data_registro)
	with open('dbInsertRegistro.txt','a') as insert_db:
		insert_db.write(insert)

def monta_linhas(pis, matricula, arquivo_nome, ponto):
	if(ponto == 'SMSI'):
		arquivo = open(arquivo_nome, 'r')
	else:
		arquivo = open(arquivo_nome, 'r')

	resultados = []
	for registro in arquivo:
		if(ponto == 'SMSI'):
			reg = re.search('(?:\d{10})(\d{2})(\d{2})(\d{4})(\d{2})(\d{2})(\d{12})', registro.replace('\n',''))
		else:
			reg = re.search('(?:\d{10})(\d{2})(\d{2})(\d{4})(\d{2})(\d{2})(\d{12})(?:.{4})', registro.replace('\n',''))
		if (reg != None):
			colaboradoPis = reg.group(6)
			if(pis == colaboradoPis):
				dia = reg.group(1)
				mes = reg.group(2)
				ano = reg.group(3)
				hora = reg.group(4)
				minuto = reg.group(5)
				insert_str = "01 N 0   %s/%s/%s %s:%s:00 %s\r\n" % (dia, mes, ano, hora, minuto, matricula.zfill(20))
				resultados.append(insert_str)
		
	arquivo.close()
	return resultados

def gera_insert_de_registro_txt(ponto_nome):
	clean_files('dbInsertRegistro.txt')
	registros = open('registros_{}.txt'.format(ponto_nome.lower()), 'r')

	numero_ponto = unidade.verificar_numero_ponto(ponto_nome)

	for registro in registros:
		resultado = re.search('(?:\d+\s[a-zA-Z]\s\w*\s+)(\d{2})\/(\d{2})\/(\d{4})\s(\d{2})\:(\d{2})\:(\d{2})\s(\d+)', registro)
		matricula = resultado.group(7)
		data_registro = '%s-%s-%s %s:%s:%s' % (resultado.group(3), resultado.group(2), resultado.group(1), resultado.group(4), resultado.group(5), resultado.group(6))
		monta_insert(matricula, data_registro, numero_ponto)

	registros.close()


def gera_arquivo(arquivo, ponto):
	nome_registro_txt = 'registros_{}.txt'.format(ponto.lower()) 
	clean_files('dbInsertRegistro.txt')
	colaboradores = open('rep_colaborador.txt', 'r')
	clean_files(nome_registro_txt)

	for colaborador in colaboradores:
		with open(nome_registro_txt, 'a') as registros_txt:
			pessoa = re.search('(?:\d\+\d\+\w\[)(\d{12})(?:\[)(.+)(?:\[\d\[\d\[)(\d+)', colaborador.replace('\n',''))
			if pessoa != None:
				registros = monta_linhas(pessoa.group(1).replace('\s',''), pessoa.group(3).replace('\s',''), arquivo, ponto)
				for registro in registros:
					registros_txt.write(registro)


if __name__ == '__main__':
	arquivo_nome = sys.argv[1]
	ponto_local = sys.argv[2].upper()
	print('Gerando arquivo registro atravez do arquivo {} e para unidade {}').format(arquivo_nome, ponto_local)
	gera_arquivo(arquivo_nome, ponto_local)
	filtrar(ponto_local)	
	gera_insert_de_registro_txt(ponto_local)