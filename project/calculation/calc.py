# encoding: utf-8
from datetime import datetime, timedelta

def calcular_parcela( parcela ):
	data_emissao_titulo = parcela.pagamento.imovel_titulo.titulo.data_emissao
	juros = taxa_juros(modulo_fiscal=parcela.pagamento.imovel_titulo.imovel.tamanho_modulo_fiscal, valor_imovel=parcela.pagamento.imovel_titulo.valor_imovel)
	if data_emissao_titulo > datetime.strptime( '10/02/2009', "%d/%m/%Y") and data_emissao_titulo < datetime.strptime( '20/05/2010', "%d/%m/%Y"):
		#artigo 12-B
		pass
	elif parcela.pagamento.data_requerimento <= parcela.data_vencimento:
		#artigo 8-B alinea a
		valor =  valor_prestacao(prestacao=parcela.valor_principal, data_vencimento=parcela.data_vencimento, data_prazo=data_emissao_titulo, juros=juros)
	elif parcela.pagamento.data_requerimento - parcela.data_vencimento <= 30:
		#artigo 8-B alinea b
		valor =  valor_prestacao(prestacao=parcela.valor_principal, data_vencimento=parcela.data_vencimento, data_prazo=data_emissao_titulo, juros=juros)
	else:
		#artigo 8-B alinea c
		prazo_prestacao = (parcela.data_vencimento - data_emissao_titulo.days
		#Na = numero de anos (inteiro) de atraso (desde o vencimento da prestacao)
		na = 2 # 2 anos e 35 dias
		#DrA = numero de dias remanescentes (apos se completar a contagem do numero de anos inteiros) ate a data do requerimento mais 30 dias
		dra = 65 # 35 dias + 30 dias
		#VPa = P x ( 1 + ( N + Na + DrA/360 ) x J/100 )
		valor = float(parcela.valor_principal) * ( 1 + ( ( float(prazo_prestacao)/360. ) + na + dra/360. ) * ( juros /100.) )

		#artigo 8-C alinea a
		#CM = porcentagem correspondente a correcao monetaria
		cm = indice_tr()
		#Ma = numero de meses (inteiro) de atraso ( decorridos desde o vencimento da prestacao )
		ma = 25
		#DrM = numero de dias remanescentes (apos se completar a contagem de numero de meses inteiros) ate a data do requerimento mais 30 dias
		drm = 35 # 5 dias + 30 dias
		#Jm = taxa de juro mensal de mora
		jm = 1
		#VFPa = VPa x ( 1 + CM + ( Ma + DrM/30 ) x Jm/100 )
		valor_encargos = valor * ( 1 + cm + ( ma + float(drm/30.) ) * jm/100.  )
		valor = valor + valor_encargos
		parcela.valor_multa = jm
		parcela.valor_correcao = cm
	parcela.valor_juro = juros
	parcela.valor_total = valor
	parcela.save()
	return parcela

def taxa_juros( modulo_fiscal, valor_imovel ):
	#artigo 9,10 - portaria 1 20/05/2010
	ijuros = 0.0
	if dados['modulo_fiscal'] > 4.:
		ijuros = 6.75
	elif dados['valor_imovel'] <= 40000:
		ijuros = 1.
	elif dados['valor_imovel'] > 40000 and dados['valor_imovel'] <= 100000:
		ijuros = 2.
	elif dados['valor_imovel'] > 100000:
		ijuros = 4.
	return ijuros

def valor_prestacao(prestacao, data_vencimento, data_prazo, juros):
	#artigo 8-B alinea a
	#N = prazo da prestacao em numero de anos
	prazo_prestacao = data_vencimento - data_prazo.days
	#VP = P x ( 1 + ( N x J/100 ) )
	return float(prestacao) * ( 1 + (float(prazo_prestacao)/360.)*( juros /100.0) )

def nossa_terra_nossa_escola(modulo_fiscal, prestacao, encargos):
	#beneficio para areas de ate 4 modulos fiscais
	if modulo_fiscal <= 4.:
		#encargos calculados com a parcela anual e depois somados a  metade do valor da parcela anual
		return encargos + ( prestacao / 2 )
	else:
		#valor integral da parcela com encargos
		return encargos + prestacao

def indice_tr():
	#periodo entre o vencimento da prestacao e a data do requerimento
	#dt_inicio: dia util anterior ao do vencimento da prestacao
	#dt_final: dia util anterior ao requerimento
	return 3.7999

def indice_igpm():
	#periodo entre o vencimento da prestacao e a data do requerimento
	#mes_inicio: anterior ao do vencimento da prestacao
	#mes_final: anterior ao do requerimento
	return 3.7999
