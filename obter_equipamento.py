import Ponto

def obter_equipamento(local):    
    if(local == "SMSI"):
        equipamento = Ponto.Ponto(local, 166, '00004002050013071')
    elif (local == 'FARMACIA'):
        equipamento = Ponto.Ponto(local, 121)
    elif (local == 'BELA_VISTA'):
        equipamento = Ponto.Ponto(local, 156)
    elif (local == 'CENTRAL_REG'):
        equipamento = Ponto.Ponto(local, 109, '00004004330005165')
    elif (local == 'CEREST'):
        equipamento = Ponto.Ponto(local, 163)
    elif (local == 'GRAJAU'):
        equipamento = Ponto.Ponto(local, 149, '00004004330003027')
    elif (local == 'IMPERADOR'):
		equipamento = Ponto.Ponto(local, 160, '00004004330005868')
    elif (local == 'MARINGA'):
		equipamento = Ponto.Ponto(local, 103)
    elif (local == 'SAO_JORGE'):
		equipamento = Ponto.Ponto(local, 144)
    elif (local == 'SAMU'):
		equipamento = Ponto.Ponto(local, 147)
    elif (local == 'UPA'):
		equipamento = Ponto.Ponto(local, 169, '00004004330016111')
    elif (local == 'MARIANA'):
		equipamento = Ponto.Ponto(local, 158)
    elif (local == 'SAO_BENEDITO'):
		equipamento = Ponto.Ponto(local, 150)
    elif (local == 'SAO_MIGUEL'):
		equipamento = Ponto.Ponto(local, 148)
    elif (local == 'TAQUARI'):
		equipamento = Ponto.Ponto(local, 155)
    elif (local == 'APARECIDA'):
		equipamento = Ponto.Ponto(local, 178)
    elif (local == 'BOM_JESUS'):
		equipamento = Ponto.Ponto(local, 179)
    elif (local == 'CIMENTOLANDIA'):
		equipamento = Ponto.Ponto(local, 180)
    elif (local == 'MATERNO'):
		equipamento = Ponto.Ponto(local, 181)
    elif (local == 'CS1'):
		equipamento = Ponto.Ponto(local, 182, '00004004330006302')
    elif (local == 'CENTRO_DIA'):
		equipamento = Ponto.Ponto(local, 183)
    elif (local == 'CAMARGO'):
		equipamento = Ponto.Ponto(local, 184)
    elif (local == 'SAO_ROQUE'):
		equipamento = Ponto.Ponto(local, 185)
    elif (local == 'SAO_CAMILO'):
		equipamento = Ponto.Ponto(local, 186)
    elif (local == 'VIRGINIA'):
		equipamento = Ponto.Ponto(local, 187, '00004004330016137')
    elif (local == 'GUARI'):
		equipamento = Ponto.Ponto(local, 188, '00004004310000100')
    elif (local == 'SANTA_MARIA'):
		equipamento = Ponto.Ponto(local, 189)
    elif (local == 'PACOVA'):
		equipamento = Ponto.Ponto(local, 190)
    elif (local == 'ALTO_BRANCAL'):
		equipamento = Ponto.Ponto(local, 191)
    elif (local == 'AGROVILA'):
		equipamento = Ponto.Ponto(local, 192)
    elif (local == 'CAPUTERA'):
		equipamento = Ponto.Ponto(local, 193)
    elif (local == 'CME'):
		equipamento = Ponto.Ponto(local, 103)
    
    return equipamento