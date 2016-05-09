# encoding: utf-8
from datetime import datetime, timedelta
from project.system.integration import consumir_tr, consumir_igpm
from project.system.models import SolicitacaoNossaTerraNossaEscola

def calcular_parcela( parcela ):
	data_emissao_titulo = parcela.pagamento.imovel_titulo.titulo.data_emissao
	modulo_fiscal = parcela.pagamento.imovel_titulo.imovel.tamanho_modulo_fiscal
	valor_imovel = parcela.pagamento.imovel_titulo.valor_imovel
	data_requerimento = parcela.pagamento.data_requerimento
	anterior_20_maio_2010 = False

	if data_emissao_titulo > datetime.strptime( '10/02/2009', "%d/%m/%Y").date() and data_emissao_titulo < datetime.strptime( '20/05/2010', "%d/%m/%Y").date():
		anterior_20_maio_2010 = True
	else:
		if data_requerimento <= parcela.data_vencimento or (data_requerimento - parcela.data_vencimento).days <= 30:
			#artigo 8-B alinea a e b
			#VP = P x ( 1 + N x J/100 )
			vp =  valor_prestacao(parcela.valor_principal, data_emissao_titulo, data_requerimento, indice_juros(modulo_fiscal, valor_imovel))
			if anterior_20_maio_2010:
				#artigo 12-B
				#AVP = VP x ( 1 + IGPM ) : valor da prestacao com os juros devidos
				vp = vp * ( 1 + indice_igpm(data_vencimento=parcela.data_vencimento, data_requerimento=data_requerimento) )
			parcela.valor_juro = vp - float(parcela.valor_principal)
			parcela.valor_multa = 0.
			parcela.valor_correcao = 0.
			parcela.valor_desconto = 0.
			parcela = nossa_terra_nossa_escola(parcela)
			parcela.valor_total = vp - parcela.valor_desconto
		else:
			#artigo 8-B alinea c
			#VPa = P x ( 1 + ( N + Na + DrA/360 ) x J/100 )
			vpa = valor_prestacao_atraso(parcela.valor_principal, data_requerimento, parcela.data_vencimento, data_emissao_titulo, indice_juros(modulo_fiscal, valor_imovel))
			#artigo 8-C alinea a
			#VFPa = VPa x ( 1 + CM + ( Ma + DrM/30 ) x Jm/100 )
			vfpa = valor_final_prestacao_atraso(vpa, data_requerimento, parcela.data_vencimento)
			if anterior_20_maio_2010:
				#artigo 12-B
				#AVFPa = VFPa x ( 1 + IGPM ) : valor final da prestacao em atraso
				vfpa = vfpa * ( 1 + indice_igpm(data_vencimento=parcela.data_vencimento, data_requerimento=data_requerimento) )
			parcela.valor_juro = vpa - float(parcela.valor_principal)
			parcela.valor_multa = 1.
			parcela.valor_correcao = vfpa - vpa
			parcela.valor_desconto = 0.
			parcela = nossa_terra_nossa_escola(parcela)
			parcela.valor_total = vfpa - parcela.valor_desconto
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

#N
def prazo_prestacao( data_emissao_titulo, data_requerimento ):
	return (data_requerimento - data_emissao_titulo).days + 5

#VP
def valor_prestacao(prestacao, data_emissao, data_requerimento, juros):
	#artigo 8-B alinea a e b
	#N = prazo da prestacao em numero de anos
	#VP = P x ( 1 + ( N x J/100 ) )
	return float(prestacao) * ( 1 + (float( prazo_prestacao(data_emissao_titulo=data_emissao, data_requerimento=data_requerimento) )/360.)*( juros /100.) )

#VPa
def valor_prestacao_atraso(prestacao, data_requerimento, data_vencimento, data_emissao_titulo, juros):
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
	return float(prestacao) * ( 1 + ( ( float( n )/360. ) + na + dra/360. ) * ( juros /100.) )

#VFPa
def valor_final_prestacao_atraso(vpa, data_requerimento, data_vencimento):
	#artigo 8-C alinea a
	#CM = porcentagem correspondente a correcao monetaria
	cm = indice_tr()
	#Ma = numero de meses (inteiro) de atraso ( decorridos desde o vencimento da prestacao )
	dt = data_requerimento - data_vencimento
	qtd_mes = dt.days/30
	qtd_dias = dt.days - qtd_mes*30
	ma = qtd_mes
	#DrM = numero de dias remanescentes (apos se completar a contagem de numero de meses inteiros) ate a data do requerimento mais 30 dias
	drm = qtd_dias + 30 # 5 dias + 30 dias
	#Jm = taxa de juro mensal de mora
	mora = 1
	#VFPa = VPa x ( 1 + CM + ( Ma + DrM/30 ) x Jm/100 )
	return vpa * ( 1 + cm + ( ma + float(drm/30.) ) * mora/100.  )

def nossa_terra_nossa_escola( parcela ):
	#beneficio para areas de ate 4 modulos fiscais
	#encargos calculados com a parcela anual e depois somados a  metade do valor da parcela anual
	if parcela.pagamento.imovel_titulo.imovel.tamanho_modulo_fiscal <= 4.:
		solicitacao = SolicitacaoNossaTerraNossaEscola.objects.filter( parcela__id = parcela.id, status = True )
		if solicitacao:
			parcela.valor_desconto = parcela.valor_principal / 2.
	return parcela

def indice_tr( data_vencimento, data_requerimento ):
	#periodo entre o vencimento da prestacao e a data do requerimento
	#dt_inicio: dia util anterior ao do vencimento da prestacao
	data_inicio = data_vencimento
	#dt_final: dia util anterior ao requerimento
	data_final = data_requerimento
	tr = consumir_tr(data_inicio=data_inicio, data_final=data_final)
	return tr/100.

def indice_igpm( data_vencimento, data_requerimento ):
	#periodo entre o vencimento da prestacao e a data do requerimento
	#mes_inicio: anterior ao do vencimento da prestacao
	mes_inicio = data_vencimento
	#mes_final: anterior ao do requerimento
	mes_final = data_requerimento
	igpm = consumir_igpm(mes_inicio=mes_inicio, mes_final=mes_final)
	return igpm/100.
