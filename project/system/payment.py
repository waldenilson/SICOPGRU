# -- coding: utf-8 --
from datetime import timedelta
from project.calculation.calc import calcular_parcela
from project.system.models import Imovel, Titulo, ImovelTitulo, Convenio, FormaPagamento, Pagamento, Parcela, ParcelaGuia, Guia
from project.core.models import Municipio
import datetime

def gerar_parcelas( dados, data_requerimento, usuario ):
	# cadastrar pagamento
	obj_pagamento = Pagamento(
			imovel_titulo= ImovelTitulo.objects.get(pk=int(dados['imovel_titulo'])),
			convenio= Convenio.objects.get(pk=1),
			data_requerimento= data_requerimento,
			forma_pagamento= FormaPagamento.objects.get(pk=2),
			creator_auth_user= usuario,
			updated_at= datetime.datetime.now(),
			updater_auth_user= usuario
		)
	obj_pagamento.save()

	for n_parcela in range(1,18):
	   # cadastrar parcela(s)
	   obj_parcela = Parcela(
			pagamento= obj_pagamento,
			numero= n_parcela,
			data_vencimento = dados['data_emissao_titulo'].replace(dados['data_emissao_titulo'].year + (n_parcela + 2) ),
			valor_principal = float(dados['valor_imovel'])/17.0,
			valor_desconto = "{0:.2f}".format(0),
			valor_deducao = "{0:.2f}".format(0),
			valor_multa = "{0:.2f}".format(0),
			valor_juro = "{0:.2f}".format(0),
			valor_acrescimo = "{0:.2f}".format(0),
			valor_correcao = "{0:.2f}".format(0),
			valor_total = float(dados['valor_imovel'])/17.0
	   )
	   obj_parcela.save()

def carregar_pagamento(cpf):
	return Pagamento.objects.filter( imovel_titulo__titulo__cpf_titulado__icontains=cpf )

def carregar_parcelas( cpf ):
	lista = carregar_pagamento( cpf )
	dados = dict()
	dados['pagamento'] = lista[0]
	parcelas = Parcela.objects.filter( pagamento__id = lista[0].id ).order_by('numero')
	l_parcelas = []
	proxima_parcela_a_pagar = 1
	for p in parcelas:
		p = calcular_parcela(p)
		parcela = dict()
		parcela['id'] = p.id
		parcela['numero'] = p.numero
		parcela['valor_principal'] = p.valor_principal
		parcela['valor_juro'] = p.valor_juro
		parcela['valor_multa'] = p.valor_multa
		parcela['valor_correcao'] = p.valor_correcao
		parcela['valor_total'] = p.valor_total
		parcela['data_vencimento'] = p.data_vencimento
		parcela['vencida'] = 'False'
		if p.pagamento.data_requerimento > p.data_vencimento:
			parcela['vencida'] = 'True'
		parcela['status'] = 'False'
		pguia = ParcelaGuia.objects.filter( parcela__id = p.id )
		for pg in pguia:
			if pg.status_pagamento:
				parcela['status'] = 'True'
		l_parcelas.append(parcela)
		#verificar a proxima parcela sucessiva a pagar
		if parcela['status'] == 'True':
			proxima_parcela_a_pagar += 1
	dados['parcelas'] = l_parcelas
	dados['proxima_parcela_a_pagar'] = proxima_parcela_a_pagar

	# retornar obj pagamento, parcelas
	return dados

def parcela_a_pagar( cpf ):
	parcelas = Parcela.objects.filter( pagamento__id = carregar_pagamento(cpf)[0].id ).order_by('numero')
	parcela = parcelas[0]
	for p in parcelas:
		if not parcela.status_pagamento:
			parcela = p
			break
	return parcela

def return_file_ref(file_ref):
	header = []
	lines = []
	x = 0
	for line in file_ref:
		if x == 0:
			header = line[0]
		else:
			lines.append(line[0])
		x += 1
	obj_convenio = Convenio.objects.filter( numero = header )
	if obj_convenio:
		print 'conv'
		for l in lines:
			guias = Guia.objects.filter( id = int(l[0:10]) )
			for g in guias:
				print 'guia'
				parcelasguia = ParcelaGuia.objects.filter( guia__id = g.id )
				for pg in parcelasguia:
					print 'parcelaguia'
					pg.status_pagamento = True
					pg.data_pagamento = str(l[10:14])+'-'+str(l[14:16])+'-'+str(l[16:18])
					pg.guia.codigo_retorno = file_ref
					pg.guia.save()
					pg.save()
	else:
		print 'no conv'

def excecao_maior_menor():
	pass

def excecao_menor_maior():
	pass
