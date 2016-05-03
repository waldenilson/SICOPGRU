# -- coding: utf-8 --
from datetime import timedelta
from project.calculation.calc import calcular
from project.system.models import Imovel, Titulo, ImovelTitulo, Convenio, FormaPagamento, Pagamento, Parcela, ParcelaGuia, Guia
from project.core.models import Municipio
import datetime

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

def iniciar_calculo( dados, data_requerimento, nossa_escola, usuario ):
	print 'INICIANDO CALCULO'

	# cadastrar titulo
	obj_titulo = Titulo(
			numero= dados['titulo'],
			tipo= dados['tipo_titulo'],
			processo= dados['processo'],
			nome_titulado= dados['nome_titulado'],
			cpf_titulado= dados['cpf_titulado'],
			data_emissao= dados['data_emissao_titulo']
		)
	obj_titulo.save()

	# cadastrar imovel
	obj_imovel = Imovel(
			nome= dados['nome_imovel'],
			sncr= dados['sncr'],
			gleba= dados['gleba'],
			area_total= dados['area_total'],
			tamanho_modulo_fiscal= dados['modulo_fiscal'],
			municipio= dados['municipio'],
			regional= dados['regional']
		)
	obj_imovel.save()

	# cadastrar imoveltitulo
	obj_ititulo = ImovelTitulo(
			imovel= obj_imovel,
			titulo= obj_titulo,
			valor_imovel= dados['valor_imovel']
		)
	obj_ititulo.save()

	# cadastrar pagamento
	obj_pagamento = Pagamento(
			imovel_titulo= obj_ititulo,
			convenio= Convenio.objects.get(pk=1),
			data_requerimento= data_requerimento,
			nossa_escola= nossa_escola,
			forma_pagamento= FormaPagamento.objects.get(pk=2),
			creator_auth_user= usuario,
			updated_at= datetime.datetime.now(),
			updater_auth_user= usuario
		)
	obj_pagamento.save()

	for i in range(1,18):
	   retorno = calcular( dados, data_requerimento, nossa_escola, i )
	   # cadastrar parcela(s)
	   obj_parcela = Parcela(
			pagamento= obj_pagamento,
			numero= retorno['numero_parcela'],
			data_vencimento= retorno['data_vencimento'],
			valor_principal= retorno['prestacao'],
			valor_desconto= retorno['desconto'],
			valor_deducao= retorno['deducao'],
			valor_multa= retorno['multa'],
			valor_juro= retorno['juros'],
			valor_acrescimo= retorno['acrescimo'],
			valor_correcao= retorno['correcao'],
			valor_total= retorno['total']
		)
	   obj_parcela.save()

def carregar_parcelas( cpf ):
	lista = Pagamento.objects.filter( imovel_titulo__titulo__cpf_titulado__icontains=cpf )
	dados = dict()
	dados['pagamento'] = lista[0]
	parcelas = Parcela.objects.filter( pagamento__id = lista[0].id )
	l_parcelas = []
	for p in parcelas:
		parcela = dict()
		parcela['id'] = p.id
		parcela['numero'] = p.numero
		parcela['valor_principal'] = p.valor_principal
		parcela['valor_juro'] = p.valor_juro
		parcela['valor_multa'] = p.valor_multa
		parcela['valor_correcao'] = p.valor_correcao
		parcela['valor_total'] = p.valor_total
		parcela['data_vencimento'] = p.data_vencimento
		parcela['status'] = 'False'
		pguia = ParcelaGuia.objects.filter( parcela__id = p.id )
		for pg in pguia:
			if pg.status_pagamento:
				parcela['status'] = 'True'
		l_parcelas.append(parcela)
	dados['parcelas'] = l_parcelas
	# retornar obj imoveltitulo, pagamento, parcelas
	return dados

def recalculo():
	pass

def excecao_maior_menor():
	pass

def excecao_menor_maior():
	pass
