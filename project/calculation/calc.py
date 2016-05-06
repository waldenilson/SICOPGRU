# encoding: utf-8
from datetime import datetime, timedelta

def calcular_parcela( parcela ):
	data_emissao_titulo = parcela.pagamento.imovel_titulo.titulo.data_emissao
	modulo_fiscal = parcela.pagamento.imovel_titulo.imovel.tamanho_modulo_fiscal
	valor_imovel = parcela.pagamento.imovel_titulo.valor_imovel
	data_requerimento = parcela.pagamento.data_requerimento
	juros = indice_juros(modulo_fiscal=modulo_fiscal, valor_imovel=valor_imovel)

	if data_emissao_titulo > datetime.strptime( '10/02/2009', "%d/%m/%Y").date() and data_emissao_titulo < datetime.strptime( '20/05/2010', "%d/%m/%Y").date():
		#artigo 12-B
		pass
	elif data_requerimento <= parcela.data_vencimento or (data_requerimento - parcela.data_vencimento).days <= 30:
		#artigo 8-B alinea a e b
		vp =  valor_prestacao(prestacao=parcela.valor_principal, data_emissao=data_emissao_titulo, data_requerimento=data_requerimento, juros=juros)
		parcela.valor_juro = vp - float(parcela.valor_principal)
		parcela.valor_multa = 0.
		parcela.valor_correcao = 0.
		parcela.valor_total = vp
	else:
		#artigo 8-B alinea c
		n = prazo_prestacao(data_requerimento=data_requerimento,data_emissao_titulo=data_emissao_titulo)
		#Na = numero de anos (inteiro) de atraso (desde o vencimento da prestacao)
		dt = data_requerimento - parcela.data_vencimento
		qtd_ano = dt.days/360
		qtd_dias = dt.days - qtd_ano*360
		na = qtd_ano # 2 anos e 35 dias (data_requerimento - parcela.data_vencimento).days/360
		#DrA = numero de dias remanescentes (apos se completar a contagem do numero de anos inteiros) ate a data do requerimento mais 30 dias
		dra = qtd_dias + 30
		#VPa = P x ( 1 + ( N + Na + DrA/360 ) x J/100 )
		vpa = valor_prestacao_atraso(prestacao=parcela.valor_principal, n=n, na=na, dra=dra, juros=juros)

		#artigo 8-C alinea a
		#CM = porcentagem correspondente a correcao monetaria
		cm = indice_tr()
		#Ma = numero de meses (inteiro) de atraso ( decorridos desde o vencimento da prestacao )
		qtd_mes = dt.days/30
		qtd_dias = dt.days - qtd_mes*30
		ma = qtd_mes
		#DrM = numero de dias remanescentes (apos se completar a contagem de numero de meses inteiros) ate a data do requerimento mais 30 dias
		drm = qtd_dias + 30 # 5 dias + 30 dias
		#Jm = taxa de juro mensal de mora
		jm = 1
		#VFPa = VPa x ( 1 + CM + ( Ma + DrM/30 ) x Jm/100 )
		valor_encargos = vpa * ( 1 + cm + ( ma + float(drm/30.) ) * jm/100.  )
		valor = vpa + valor_encargos
		parcela.valor_juro = vpa - float(parcela.valor_principal)
		parcela.valor_multa = jm
		parcela.valor_correcao = valor_encargos - vpa
		parcela.valor_total = valor_encargos
	parcela.save()
	return parcela

def indice_juros( modulo_fiscal, valor_imovel ):
	#artigo 9,10 - portaria 1 20/05/2010
	ijuros = 0.0
	if modulo_fiscal > 4.:
		ijuros = 6.75
	elif valor_imovel <= 40000:
		ijuros = 1.
	elif valor_imovel > 40000 and valor_imovel <= 100000:
		ijuros = 2.
	elif valor_imovel > 100000:
		ijuros = 4.
	return ijuros

def prazo_prestacao( data_emissao_titulo, data_requerimento ):
	return (data_requerimento - data_emissao_titulo).days

def valor_prestacao(prestacao, data_emissao, data_requerimento, juros):
	#artigo 8-B alinea a e b
	#N = prazo da prestacao em numero de anos
	#VP = P x ( 1 + ( N x J/100 ) )
	return float(prestacao) * ( 1 + (float( prazo_prestacao(data_emissao_titulo=data_emissao, data_requerimento=data_requerimento) )/360.)*( juros /100.) )

def valor_prestacao_atraso(prestacao, n, na, dra, juros):
	#artigo 8-B alinea c
	#VPa = P x ( 1 + ( N + Na + DrA/360 ) x J/100 )
	return float(prestacao) * ( 1 + ( ( float( n )/360. ) + na + dra/360. ) * ( juros /100.) )

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
	return 2.5/100.

def indice_igpm():
	#periodo entre o vencimento da prestacao e a data do requerimento
	#mes_inicio: anterior ao do vencimento da prestacao
	#mes_final: anterior ao do requerimento
	return 2.5/100.
