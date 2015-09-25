# encoding: utf-8
from datetime import datetime

def get_codigo_banco():
	return '001'

def get_moeda():
	return '9'

def get_data_base():
	return datetime(day=7,month=10,year=1997)

def get_DV_codigo_barra():
	return '5'

def get_DV_campo_1():
	return '7'

def get_DV_campo_2():
	return '8'

def get_DV_campo_3():
	return '9'

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
	retorno = str(get_codigo_banco())+str(get_moeda())+str(get_DV_codigo_barra())+str(get_fator_vencimento(dt_vencimento))+str(valor)+str(get_zeros())+str(get_convenio())+str(get_nosso_numero())+str(get_carteira())
	return retorno

def calcular_linha_digitavel(codigo_barra, valor, dt_vencimento):
	posicao_20_24_codigo_barra = codigo_barra[19:24]
	posicao_25_34_codigo_barra = codigo_barra[24:34]
	posicao_35_44_codigo_barra = codigo_barra[34:44]
	retorno = str(get_codigo_banco())+str(get_moeda())+str(posicao_20_24_codigo_barra)+str(get_DV_campo_1())+str(posicao_25_34_codigo_barra)+str(get_DV_campo_2())+str(posicao_35_44_codigo_barra)+str(get_DV_campo_3())+str(get_DV_codigo_barra())+str(get_fator_vencimento(dt_vencimento))+str(valor)
	return retorno
