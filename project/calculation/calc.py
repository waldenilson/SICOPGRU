# encoding: utf-8
from datetime import timedelta

def calcular( dados, data_requerimento, numero_parcela ):

	prestacao = float(dados['valor_imovel'])/17.0
	imulta = 1.0

	if dados['modulo_fiscal'] > 4:
		ijuros = 6.75
	else:
		if dados['valor_imovel'] <= 40000:
			ijuros = 1.0
		else:
			if dados['valor_imovel'] > 40000 and dados['valor_imovel'] <= 100000:
				ijuros = 2.0
			else:
				if dados['valor_imovel'] > 100000:
					ijuros = 4.0

	return verificar_vencimento( data_requerimento, ijuros, prestacao, numero_parcela, imulta, dados )

def verificar_vencimento( data_requerimento,
	ijuros,
	prestacao,
	numero_parcela,
	imulta,
	dados):

	correcao = 0
	multa = 0
	juros = 0
	desconto = 0
	valor_prestacao = 0
	valor_prestacao_corrigido = 0
	valor_final_prestacao = 0
	data_vencimento = dados['data_emissao_titulo'].replace(dados['data_emissao_titulo'].year+3)


	if dados['data_emissao_titulo'] > '10/02/2009' and dados['data_emissao_titulo'] < '20/05/2010':
		#artigo 12-B
		pass
	else:
		if data_requerimento <= data_vencimento:
			#artigo 8-B alinea a
			valor_prestacao =  calculo_prazo_prestacao(prestacao=prestacao, data_vencimento=data_vencimento, data_prazo=dados['data_emissao_titulo'], ijuros=ijuros)
		else:
			if data_requerimento - data_vencimento <= 30:
				#artigo 8-B alinea b
				valor_prestacao =  calculo_prazo_prestacao(prestacao=prestacao, data_vencimento=data_vencimento, data_prazo=dados['data_emissao_titulo'], ijuros=ijuros)
			else:
				#artigo 8-B alinea c
				prazo_prestacao = (data_vencimento - dados['data_emissao_titulo']).days
				#Na = numero de anos (inteiro) de atraso (desde o vencimento da prestacao)
				na = 2 # 2 anos e 35 dias
				#DrA = numero de dias remanescentes (apos se completar a contagem do numero de anos inteiros) ate a data do requerimento mais 30 dias
				dra = 65 # 35 dias + 30 dias
				#VPa = P x ( 1 + ( N + Na + DrA/360 ) x J/100 )
				valor_prestacao = float(prestacao) * ( 1 + ( ( float(prazo_prestacao)/360. ) + na + dra/360. ) * (ijuros/100.0) )

				#artigo 8-C alinea a
				#CM = porcentagem correspondente a correcao monetaria
				cm = calculo_tr()
				#Ma = numero de meses (inteiro) de atraso ( decorridos desde o vencimento da prestacao )
				ma = 25
				#DrM = numero de dias remanescentes (apos se completar a contagem de numero de meses inteiros) ate a data do requerimento mais 30 dias
				drm = 35 # 5 dias + 30 dias
				#Jm = taxa de juro mensal de mora
				jm = 1
				#VFPa = VPa x ( 1 + CM + ( Ma + DrM/30 ) x Jm/100 )
				valor_prestacao_corrigido = valor_prestacao * ( 1 + cm + ( ma + float(drm/30.) ) * jm/100  )
				valor_final_prestacao = valor_prestacao + valor_prestacao_corrigido
				correcao = cm
	return True


def calculo_prazo_prestacao(prestacao, data_vencimento, data_prazo, ijuros):
	#artigo 8-B alinea a
	#N = prazo da prestacao em numero de anos
	prazo_prestacao = data_vencimento - data_prazo.days
	#VP = P x ( 1 + ( N x J/100 ) )
	return float(prestacao) * ( 1 + (float(prazo_prestacao)/360.)*(ijuros/100.0) )

def calculo_nossa_terra_nossa_escola(prestacao, encargos):
	#encargos calculados com a parcela anual e depois somados a  metade do valor da parcela anual
	return encargos + ( prestacao / 2 )

def calculo_tr():
	#periodo entre o vencimento da prestacao e a data do requerimento
	#dt_inicio: dia util anterior ao do vencimento da prestacao
	#dt_final: dia util anterior ao requerimento
	return 3.7999

def calculo_igpm():
	#periodo entre o vencimento da prestacao e a data do requerimento
	#mes_inicio: anterior ao do vencimento da prestacao
	#mes_final: anterior ao do requerimento
	return 3.7999
