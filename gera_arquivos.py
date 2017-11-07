# -*- coding: iso8859-1 -*-
import re
import time
import sys

def clean_files(fileName):
	file = open(fileName, 'w')
	file.write('')
	file.close()

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

def verificar_numero_ponto(ponto):
	if(ponto == 'SMSI'):
		return 166
	elif (ponto == 'FARMACIA'):
		return 121
	elif (ponto == 'BELA_VISTA'):
		return 156
	elif (ponto == 'CENTRAL_REG'):
		return 109
	elif (ponto == 'CEREST'):
		return 163
	elif (ponto == 'GRAJAU'):
		return 149
	elif (ponto == 'IMPERADOR'):
		return 160
	elif (ponto == 'MARINGA'):
		return 103
	elif (ponto == 'SAO_JORGE'):
		return 144
	elif (ponto == 'SAMU'):
		return 147
	elif (ponto == 'UPA'):
		return 169
	elif (ponto == 'MARIANA'):
		return 158
	elif (ponto == 'SAO_BENEDITO'):
		return 150
	elif (ponto == 'SAO_MIGUEL'):
		return 148
	elif (ponto == 'TAQUARI'):
		return 155
	elif (ponto == 'APARECIDA'):
		return 178
	elif (ponto == 'BOM_JESUS'):
		return 179
	elif (ponto == 'CIMENTOLANDIA'):
		return 180
	elif (ponto == 'MATERNO'):
		return 181

def gera_insert_de_registro_txt(ponto_nome):
	clean_files('dbInsertRegistro.txt')
	registros = open('registros_{}.txt'.format(ponto_nome.lower()), 'r')

	numero_ponto = verificar_numero_ponto(ponto_nome)

	for registro in registros:
		resultado = re.search('(?:\d+\s[a-zA-Z]\s\w*\s+)(\d{2})\/(\d{2})\/(\d{4})\s(\d{2})\:(\d{2})\:(\d{2})\s(\d+)', registro)
		matricula = resultado.group(7)
		data_registro = '%s-%s-%s %s:%s:%s' % (resultado.group(3), resultado.group(2), resultado.group(1), resultado.group(4), resultado.group(5), resultado.group(6))
		monta_insert(matricula, data_registro, numero_ponto)

	registros.close()


def gera_arquivo(arquivo, ponto):
	nome_registro_txt = 'registros_{}.txt'.format(ponto.lower()) 
	clean_files(nome_registro_txt)
	clean_files('dbInsertRegistro.txt')
	colaboradores = open('rep_colaborador.txt', 'r')

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
	gera_insert_de_registro_txt(ponto_local)