# -*- coding: iso8859-1 -*-
import re
import time
from datetime import datetime
import sys
import verifica_codigo_unidade as unidade

def clean_files(filename):
	file = open(filename, 'w')
	file.write('')
	file.close()

def lista_refatorada(filename, mes, ano, atual=False):
	lista = []

	if(not atual):
		if (mes == "01"):
			mes = "12"
			ano = int(ano) - 1
		else:
			mes = int(mes) - 1

	expr = '01\sN\s0\s+\d{2}\/%s\/%s\s\d{2}:\d{2}:\d{2}\s\d{20}' % (mes, ano)
	with open(filename, 'r') as arquivo:
		for linha in arquivo:
			item = re.search(expr, linha)
			if item != None:
				lista.append(item.group()+"\r\n")

	return lista

def filtrar(ponto_nome):
	filename = 'registros_{}.txt'.format(ponto_nome.lower())
	current_month = datetime.now().strftime('%m')
	current_year = datetime.now().strftime('%Y')
	anterior = lista_refatorada(filename, current_month, current_year)
	atual = lista_refatorada(filename, current_month, current_year, True)
			
	clean_files(filename)

	with open(filename, 'a') as arquivo:
		for item in anterior:
			arquivo.write(item)

	with open(filename, 'a') as arquivo:
		for item in atual:
			arquivo.write(item)

def monta_insert(colaborado_matricula, data_registro, numero_ponto):
	insert = "INSERT INTO HE22 VALUES(NULL,'%s','%s','0','0','0','2','0','4','255','1','%s','0','0','4','0','0');\n" % (numero_ponto,colaborado_matricula, data_registro);
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
	