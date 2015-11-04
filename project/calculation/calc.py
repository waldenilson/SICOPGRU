# encoding: utf-8
from datetime import timedelta

def calcular( dados, data_requerimento, nossa_escola, numero_parcela ):

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

	print 'ESTA CALCULANDO'

	return verificar_vencimento( data_requerimento, ijuros, prestacao, numero_parcela, imulta, nossa_escola, dados )

def verificar_vencimento( data_requerimento,
	ijuros,
	prestacao,
	numero_parcela,
	imulta,
	nossa_escola,
	dados):

	correcao = 0
	principal = 0 
	principal_juros_correcao = 0
	multa = 0
	desconto = 0
	principal_corrigido_desconto = 0
	principal_corrigido_multa = 0
	dtgeracao = None
	stgerada =False
	data = None

	data_vencimento = dados['data_emissao_titulo'].replace(dados['data_emissao_titulo'].year+3)
	
	if data_requerimento <= data_vencimento: # nao vencido
		print "nao vencido"
		if (data_vencimento - data_requerimento).days < 30:
			#incide juros de emissao titulo ateh vencimento parcela
			dias_juros = (data_vencimento - dados['data_emissao_titulo']).days
			dtvencGRU = data_vencimento
			print "dias_juros ",(dias_juros)
			juros = float(prestacao)*((float(dias_juros)/360.)*(ijuros/100.0))
			prestacao_juros = prestacao + juros
			principal_corrigido = prestacao_juros
			#imprime(prestacao_juros,"prestacao_juros")
			
		else:
			if (data_vencimento - data_requerimento).days > 30:
				print "nao vencido - mais de 30 dias"   
				#incide juros de emissao titulo ate dtrequerimento + 30 dias
				dias_juros = (data_requerimento - dados['data_emissao_titulo']).days + 30
				dtvencGRU = data_requerimento + timedelta(30)
				juros = float(prestacao)*((float(dias_juros)/360.)*(ijuros/100.0))
				prestacao_juros = prestacao + juros
				principal_corrigido = prestacao_juros
				
				#imprime(prestacao_juros,"prestacao_juros")
				print "dias_juros " ,dias_juros,"prestacao ",prestacao," ijuros ",ijuros
				print "juros ",juros			
	else:
		if data_requerimento > data_vencimento: # vencido
			print"vencido "
			print"prestacao" ,prestacao
			#incide multa,correcao (a partir do dtVencParcela ) e juros (apartir de dtEmissaoTitulo)
			# juros de emissao ateh dtrequerimento + 30 dias - incidencia aa
			dias_juros = (data_requerimento - dados['data_emissao_titulo']).days + 30
			dtvencGRU = data_requerimento + timedelta(30)
			juros = float(prestacao)*((float(dias_juros)/360.)*(ijuros/100.0))
			print "juros ",juros
			prestacao_juros = prestacao + juros
			print "prestacao_juros",prestacao_juros			

			# correcao de vencimento ate dtrequerimento + 30 dias
			# falta obter a correcao correta a ser aplicada de acordo com tabela do governo
			dias_correcao = (data_requerimento - data_vencimento).days + 30
			
			#calcular o indice de correcao
			icorrecao = calculo_tr()

			correcao = prestacao_juros*((icorrecao/100.0))
			print"correcao",correcao
			print "icorrecao",icorrecao
			principal_juros_correcao = prestacao_juros + correcao
			
			# multa de vencimento ateh dtrequerimento + 30 dias
			multa = ((float(dias_correcao))/30)*float(imulta)/100*float(principal_juros_correcao)  
			principal_corrigido = principal_juros_correcao + multa
			
			print "principal_corrigido ", principal_corrigido
			print "dtvencGRU ",dtvencGRU
			print "multa",multa
	
	#referencia = str(instance.numero_processo[0:5])+str(instance.id_req[2:6])+str(numero_parcela)+str(0) #mudar qdo titulo vier do sisterleg
	
	if nossa_escola:
		desconto = principal_corrigido / 2
		principal_corrigido = desconto

	retorno = dict()
	retorno['numero_parcela'] = numero_parcela
	retorno['data_vencimento'] = dtvencGRU.replace(dtvencGRU.year + (numero_parcela - 1) )
	retorno['prestacao'] = "{0:.2f}".format(prestacao)
	retorno['desconto'] = "{0:.2f}".format(desconto)
	retorno['multa'] = "{0:.2f}".format(multa)
	retorno['juros'] = "{0:.2f}".format(juros)
	retorno['deducao'] = "{0:.2f}".format(0)
	retorno['acrescimo'] = "{0:.2f}".format(0)
	retorno['correcao'] = "{0:.2f}".format(correcao)
	retorno['total'] = "{0:.2f}".format(principal_corrigido)

	#ateh aqui
	return retorno
   
def calculo_tr():
	return 3.7999
