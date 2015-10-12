# -- coding: utf-8 --
from project.core.funcoes import consumir_url_json
from project.system.models import Tbextrato, Titulo

def consultar(cpf):

	lista = Titulo.objects.filter( cpf_titulado__icontains=cpf )
	dados = dict()
	if lista:
		dados['dados'] = 'local'
		dados['nome_titulado'] = lista[0].nome_titulado
		return dados 
	else:
		dados = consumir_base_extrato(cpf) # mudar somente aqui os metodos de consumo dos dados
		if dados != None:
			return dados
		else:
			return None

def salvar():
	pass

def consumir_base_extrato(cpf):
	lista = Tbextrato.objects.filter(cpf_req__icontains=cpf) #, situacao_processo__icontains = 'Titulado')
	dados = dict()
	if lista:
		dados['dados'] = 'externa'
		dados['nome_titulado'] = lista[0].nome_req
		dados['situacao'] = lista[0].situacao_processo
		return dados 
	else:
		return None
def consumir_sisterleg( search ):
	return consumir_sisterleg_qsit( search )

def consumir_sisterleg_qsit( search ):
	
	URL = 'http://mda.qsit.com.br/api/'
	TOKEN = '6oVBmLr5X1Aj7xr1yP3C0X5heXmdjitF'
	SISTEMA = 'sisterleg'
	TIPO = 'json'
	CPF = search
	
	return consumir_url_json( URL+'?token='+TOKEN+'&sistema='+SISTEMA+'&tipo='+TIPO+'&cpf='+CPF )

def consumir_sigef_destinacao():
	pass