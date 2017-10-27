import urllib2

def login_ponto():
	url = 'http://192.168.50.50/rep.html?pgCode=7&opType=1&lblId=0&lblLogin=rep&lblPass=121314'
	urllib2.urlopen(url)

def comunica_ponto(data_inicial, hora_inicial, data_final, hora_final):
	login_ponto()
	print data_inicial, hora_inicial, data_final, hora_final
	site = 'http://192.168.50.50/'
	get = 'rep.html?pgCode=8&opType=5&lblId=2&visibleDiv=communication&lblNsrI=000000001&lblNsrF=000046605&lblDataI=%s+%s&lblDataF=%s+%s' % (data_inicial, hora_inicial, data_final, hora_final)
	url = site+get
	file = urllib2.urlopen(url)
	data = file.read()
	print '%s b' % (len(data))
		
	with open("registros_smsi.txt", "wb") as code:
	   	if (len(data) < 25000):
	   		code.write(data)
	   	else:
	   		code.write('')

	file.close()

if __name__ == '__main__':
	pass
 