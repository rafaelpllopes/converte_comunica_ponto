# -*- coding: iso8859-1 -*-
import firebirdsql as data_base

class DB:
    """ Classe que traz a conexao com o banco de dados"""
	
    def __init__(self):
      self.conexao = data_base.connect(dsn='192.168.50.6:/home/henry/Henry.fdb', user='SYSDBA', password='masterkey')
    
    def get_conexao(self):
      return self.conexao
    
    def verificar_registro(self, matricula, registro):
      sql = "SELECT * FROM HE22 WHERE HE22_ST_MATRICULA = '%s' AND HE22_DT_REGISTRO = '%s'" % (matricula, registro)
      cursor = self.get_conexao().cursor()
      cursor.execute(sql)
      resultado = cursor.fetchone()
      cursor.close()
      existe = resultado != None
      return existe

    def inserir_registro(self, sql):
      inserir = self.get_conexao().cursor()
      inserir.execute(sql)
      self.get_conexao().commit()
      inserir.close()
    
    def obter_registros_periodo(self, ponto, ano, mes, dia):
      sql = "SELECT DISTINCT * FROM HE22 WHERE HE22_NR_EQUIP = '%s' AND HE22_DT_REGISTRO between '%s-%s-01 00:00' AND '%s-%s-%s 23:59'" % (ponto, ano, mes, ano, mes, dia)
      cursor = self.get_conexao().cursor()
      cursor.execute(sql)
      resultados = cursor.fetchall()
      cursor.close()
      return resultados

    def obter_todos_registros_funcionario(self, matricula):
      sql = "SELECT DISTINCT p.HE02_ST_NOME, r.HE22_ST_MATRICULA, r.HE22_DT_REGISTRO, e.HE01_ST_DESC FROM he22 r INNER JOIN HE02 p ON (r.HE22_ST_MATRICULA = p.HE02_ST_MATRICULA) INNER JOIN HE01 e ON (r.HE22_NR_EQUIP = e.HE01_AT_COD) WHERE r.HE22_ST_MATRICULA = '{}' ORDER BY r.HE22_DT_REGISTRO DESC".format(matricula)
      cursor = self.get_conexao().cursor()
      cursor.execute(sql)
      resultados = cursor.fetchall()
      cursor.close()
      return resultados
