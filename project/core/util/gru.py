# encoding: utf-8
from datetime import datetime

def get_codigo_banco():
	return '001'

def get_moeda():
	return '9'

def get_data_base():
	return datetime(day=7,month=10,year=1997)

#PARAMETRO CODIGO_BARRA COM 43 POSICOES. EXCLUIDO A POSICAO 5 QUE EH O DV CALCULADO AQUI
def get_DV_codigo_barra(codigo_barra):

	#NUMEROS MULTIPLICADORES DE 2 A 9 COMECANDO CONTAGEM DE TRAS PARA FRENTE NO TOTAL DE 43 POSICOES
	multiplicadores = '43290876543298765432987654329876543298765432'
	resultado_multiplicacao = []
	soma_total = 0

	#MULTIPLICACAO ENTRE CADA POSICAO DO CODIGO_BARRA COM SEU MULTIPLICADOR E SOMANDO OS RESULTADOS
	x = 0
	for cod in codigo_barra:
		resultado = int(cod)*int(multiplicadores[x])
		soma_total += resultado
		resultado_multiplicacao.append(resultado)
		x += 1

	#DIVIDE-SE A SOMA POR 11, OBTENDO O RESTO E COMO RESULTADO_FINAL A SUBTRACAO POR 11
	resto = soma_total % 11
	resultado_final = 11 - resto

	#CASO O RESULTADO_FINAL SEJA 0, 10 OU 11, O DV DO CODIGO DE BARRA SERA 1
	retorno = 1
	if resultado_final != 10 and resultado_final != 11 and resultado_final != 0:
		retorno = resultado_final

	return str(retorno)

def get_DV_campo(campo, pre_linha_digitavel):

	if campo == 1:
		cp = pre_linha_digitavel[0:9]
		multiplicadores = '212121212'
	elif campo == 2:
		cp = pre_linha_digitavel[9:19]
		multiplicadores = '1212121212'
	elif campo == 3:
		cp = pre_linha_digitavel[19:29]
		multiplicadores = '1212121212'
	
	soma_total = 0

	x = 0
	for cod in cp:
		resultado = int(cod)*int(multiplicadores[x])
		if resultado > 9:
			resultado = int(str(resultado)[0]) + int(str(resultado)[1])
		soma_total += resultado
		x += 1

	prox_dezena = 10
	achou_prox_dezena = False
	prox = soma_total
	while not achou_prox_dezena:
		if prox > 9 and str(prox)[1] == '0':
			achou_prox_dezena = True
			prox_dezena = prox
			break
		else:
			prox += 1

	retorno = str(prox_dezena - soma_total)
	return retorno

#parameter dt_vencimento type datetime.datetime
def get_fator_vencimento(dt_vencimento):
	return ( dt_vencimento - get_data_base() ).days

def get_zeros():
	return '000000'

def get_convenio():
	return '1234567'

def get_nosso_numero():
	return '1234567890'

def get_carteira():
	return '18'

def calcular_codigo_barra(valor, dt_vencimento):
	codigo_barra_sem_DV = str(get_codigo_banco())+str(get_moeda())+'0'+str(get_fator_vencimento(dt_vencimento))+str(valor)+str(get_zeros())+str(get_convenio())+str(get_nosso_numero())+str(get_carteira())
	DV_codigo_barra = get_DV_codigo_barra( codigo_barra_sem_DV )
	retorno = str(get_codigo_banco())+str(get_moeda())+str(DV_codigo_barra)+str(get_fator_vencimento(dt_vencimento))+str(valor)+str(get_zeros())+str(get_convenio())+str(get_nosso_numero())+str(get_carteira())
	return retorno

def calcular_linha_digitavel(codigo_barra, valor, dt_vencimento):
	posicao_20_24_codigo_barra = codigo_barra[19:24]
	posicao_25_34_codigo_barra = codigo_barra[24:34]
	posicao_35_44_codigo_barra = codigo_barra[34:44]

	DV_campo_1 = get_DV_campo(1, str(get_codigo_banco())+str(get_moeda())+str(posicao_20_24_codigo_barra)+str(posicao_25_34_codigo_barra)+str(posicao_35_44_codigo_barra) )
	DV_campo_2 = get_DV_campo(2, str(get_codigo_banco())+str(get_moeda())+str(posicao_20_24_codigo_barra)+str(posicao_25_34_codigo_barra)+str(posicao_35_44_codigo_barra) )
	DV_campo_3 = get_DV_campo(3, str(get_codigo_banco())+str(get_moeda())+str(posicao_20_24_codigo_barra)+str(posicao_25_34_codigo_barra)+str(posicao_35_44_codigo_barra) )

	retorno = str(get_codigo_banco())+str(get_moeda())+str(posicao_20_24_codigo_barra)+DV_campo_1+str(posicao_25_34_codigo_barra)+DV_campo_2+str(posicao_35_44_codigo_barra)+DV_campo_3+str(get_DV_codigo_barra(codigo_barra))+str(get_fator_vencimento(dt_vencimento))+str(valor)
	return retorno
