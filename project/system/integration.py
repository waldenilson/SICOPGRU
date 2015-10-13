# -- coding: utf-8 --
from project.core.funcoes import consumir_url_json
from project.system.models import Tbextrato, ImovelTitulo
from project.core.models import Municipio, Regional
from decimal import Decimal

def consultar(cpf):

	lista = ImovelTitulo.objects.filter( titulo__cpf_titulado__icontains=cpf )
	dados = dict()
	if lista:
		dados['dados'] = 'local'
		dados['nome_titulado'] = lista[0].titulo.nome_titulado
		dados['cpf_titulado'] = lista[0].titulo.cpf_titulado
		dados['titulo'] = lista[0].titulo.numero
		dados['processo'] = lista[0].titulo.processo
		dados['tipo_titulo'] = lista[0].titulo.tipo
		dados['data_emissao_titulo'] = lista[0].titulo.data_emissao
		
		dados['nome_imovel'] = lista[0].imovel.nome
		dados['sncr'] = lista[0].imovel.sncr
		dados['gleba'] = lista[0].imovel.gleba
		dados['area_total'] = lista[0].imovel.area_total
		dados['municipio'] = lista[0].imovel.municipio.nome_mun
		dados['regional'] = lista[0].imovel.regional.nome				
		dados['modulo_fiscal'] = lista[0].imovel.tamanho_modulo_fiscal

		dados['valor_imovel'] = lista[0].valor_imovel.quantize(Decimal('1.00'))
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
		dados['titulo'] = lista[0].id_req
		dados['processo'] = lista[0].numero_processo
		dados['tipo_titulo'] = 'TD'
		dados['data_emissao_titulo'] = lista[0].data_vencimento_primeira_prestacao.replace(lista[0].data_vencimento_primeira_prestacao.year - 3)

		dados['situacao'] = lista[0].situacao_processo

		dados['nome_imovel'] = lista[0].nome_imovel
		dados['sncr'] = lista[0].sncr
		dados['gleba'] = lista[0].nome_gleba
		dados['area_total'] = lista[0].area_total_imovel
		dados['municipio'] = Municipio.objects.filter( nome_mun = lista[0].nome_municipio )[0]
		dados['regional'] = Regional.objects.get(pk=1)				
		dados['modulo_fiscal'] = lista[0].tamanho_modulos_fiscais

		dados['valor_imovel'] = lista[0].valor_imovel.quantize(Decimal('1.00'))
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