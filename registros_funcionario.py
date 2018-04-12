# -*- coding: UTF-8 -*-
import sys
import DB

def traz_registros():
    db = DB.DB()
    with open("profissionais.txt", "r") as profissionais:
        for profissional in profissionais:
            func = profissional.split(",")
            matricula = func[0]
            print("Pegando registros do profissional {} com matricula {}".format(func[1].replace('\n',''), func[0].replace('\n','')))
            registros = db.obter_todos_registros_funcionario(matricula.zfill(20))
            
            with open("registros_funcionarios.txt", "a") as arquivo:
                arquivo.write("----------{} - {}----------\r\n".format(func[0].replace('\n',''), func[1].replace('\n','')))
                arquivo.write("Matricula, Registro, Local\r\n".upper())
                for registro in registros:
                    arquivo.write("{}, {}, {}\r\n".format(registro[1], registro[2], registro[3]))

if __name__ == '__main__':
    traz_registros()
