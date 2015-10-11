# -- coding: utf-8 --
from project.core.funcoes import consumir_url_json

def consultar():
	pass

def salvar():
	pass

def consumir_base_local():
	pass

def consumir_sisterleg( search ):
	return consumir_sisterleg_qsit( search )

def consumir_sisterleg_qsit( cpf ):
	
	URL = 'http://mda.qsit.com.br/api/'
	TOKEN = '6oVBmLr5X1Aj7xr1yP3C0X5heXmdjitF'
	SISTEMA = 'sisterleg'
	TIPO = 'json'
	CPF = search
	
	return consumir_url_json( URL+'?token='+TOKEN+'&sistema='+SISTEMA+'&tipo='+TIPO+'&cpf='+CPF )

def consumir_sigef_destinacao():
	pass