# -- coding: utf-8 --
from project.core.funcoes import consumir_url_json
from project.system.models import Tbextrato, ImovelTitulo

def consultar(cpf):

	lista = ImovelTitulo.objects.filter( titulo__cpf_titulado__icontains=cpf )
	dados = dict()
	if lista:
		dados['dados'] = 'local'
		dados['nome_titulado'] = lista[0].titulo.nome_titulado
		dados['cpf_titulado'] = lista[0].titulo.cpf_titulado
		dados['modulo_fiscal'] = lista[0].imovel.tamanho_modulo_fiscal
		dados['valor_imovel'] = lista[0].imovel.valor_imovel.quantize(Decimal('1.00'))
		dados['data_emissao_titulo'] = lista[0].titulo.data_emissao
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
		dados['cpf_titulado'] = lista[0].cpf_req
		dados['situacao'] = lista[0].situacao_processo
		dados['modulo_fiscal'] = lista[0].tamanho_modulos_fiscais
		dados['valor_imovel'] = lista[0].valor_imovel.quantize(Decimal('1.00'))
		dados['data_emissao_titulo'] = lista[0].data_vencimento_primeira_prestacao.replace(lista[0].data_vencimento_primeira_prestacao.year - 3)
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