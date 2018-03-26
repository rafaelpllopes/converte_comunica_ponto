import Ponto

def obter_equipamento(local):    
    if(local == "SMSI"):
        equipamento = Ponto.Ponto(local, 166, 'rep_00004002050013071.txt')
        
    return equipamento