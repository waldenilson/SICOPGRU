# -- coding: utf-8 --
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from project.system.models import Tbextrato, Parcela, ParcelaGuia, Guia
from project.core.models import Municipio, AuthUser
from decimal import Decimal
from datetime import date
from project.core.funcoes import formatDataToText
from django.contrib import messages
import datetime
from datetime import timedelta
import time
from django.http.response import HttpResponseRedirect, HttpResponse
from django.template import loader, Context
import os
from os.path import abspath, join, dirname
from django.conf import settings
from django.template.loader import get_template
from django.template import loader
from project.system.integration import consultar
from project.system.payment import iniciar_calculo, carregar_parcelas, return_file_ref
from project.core.funcoes import gerar_codigo_barra, gerar_pdf, emitir_documento, upload_file, reader_csv
from project.calculation.gru import calcular_codigo_barra, calcular_linha_digitavel

#@permission_required('system.consulta_unica', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta_unica(request):

    if request.method == "POST":
        cpf = request.POST['cpf'].replace('.','').replace('/','').replace('-','')

        if cpf != '00000000000':    
            dados = consultar(cpf)

            if dados != None:
                print 'Encontrou registro'
                if dados['dados'] == 'local':
                    lista_parcela = carregar_parcelas( cpf )
                    return HttpResponseRedirect('/sistema/parcelas-pagamento/'+dados['cpf_titulado']+'/')
                elif dados['dados'] == 'externa':
                    if dados['situacao'] == 'Titulado':
                        if dados['modulo_fiscal'] >= 1.0:
                            return HttpResponseRedirect('/sistema/inicio-pagamento/'+dados['cpf_titulado']+'/')
                        else:
                            messages.add_message(request, messages.WARNING, 'Título isento de pagamento. Abaixo de 1 módulo fiscal.')                    
                    else:
                        messages.add_message(request, messages.WARNING, 'Requerente ainda não titulado.')
            else:
                messages.add_message(request, messages.WARNING, 'CPF não encontrado.')
        else:
            messages.add_message(request, messages.WARNING, 'CPF Inválido.')
        
    return render_to_response('system/consulta_unica.html',{}, context_instance = RequestContext(request))

@permission_required('system.consulta_titulado', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta_titulado(request):
    print 'consultar e retornar titulados por cpf e/ou nome.'
    return render_to_response('system/consulta_titulado.html',{}, context_instance = RequestContext(request))

def inicio_pagamento(request, cpf):
    dados = consultar(cpf)
    if request.method == "POST":
        data_requerimento = datetime.datetime.strptime( request.POST['data_requerimento'],'%d/%m/%Y')
        data_requerimento = data_requerimento.date()
        if data_requerimento <= datetime.datetime.now().date():
            iniciar_calculo( dados, data_requerimento, request.POST.get('nossa_escola',False), AuthUser.objects.get(pk=request.user.id) )
            return HttpResponseRedirect('/sistema/parcelas-pagamento/'+cpf+'/')
        else:
            messages.add_message(request, messages.WARNING, 'Data do Requerimento maior que a data de hoje.')
    return render_to_response('system/calculo_pagamento.html',{'dados':dados}, context_instance = RequestContext(request))

def parcelas_pagamento(request, cpf):
    return render_to_response('system/parcelas.html',{'dados':carregar_parcelas( cpf )}, context_instance = RequestContext(request))

def gru_pagamento(request, id):

    # id da parcela
    parcela = Parcela.objects.get(pk=id)

    #VARIAVEIS DA GRU
#    valor_gru = '0000000175'
#    dt_vencimento = datetime.datetime.now()

    #salvar guia
    obj_guia = Guia(
        id_convenio = parcela.numero,# models.IntegerField()#primary_key
        codigo_barra = '', #models.TextField()
        codigo_linha_digitavel = '', #models.TextField()
        codigo_retorno = ''
        )
    obj_guia.save()

    #salvar parcela_guia
    obj_parcela_guia = ParcelaGuia(
        parcela = parcela,
        guia = obj_guia,
        data_pagamento = None,
        status_pagamento = False
        )
    obj_parcela_guia.save()

    #CRIACAO DOS NUMEROS E CODIGO DE BARRA
    num_codigo_barra = calcular_codigo_barra(parcela.valor_total, obj_guia.id, parcela.data_vencimento)
    num_codigo_linha_digitavel = calcular_linha_digitavel(num_codigo_barra,parcela.valor_total, parcela.data_vencimento)
    codigo_barra = gerar_codigo_barra(num_codigo_barra)

    obj_guia.codigo_barra = num_codigo_barra
    obj_guia.codigo_linha_digitavel = num_codigo_linha_digitavel
    obj_guia.save()

    print 'barra: '+num_codigo_barra+' - '+str(len(num_codigo_barra))
    print 'linha: '+num_codigo_linha_digitavel+' - '+str(len(num_codigo_linha_digitavel))

    #CRIACAO DA GRU PDF
    dados = {
                'icone':abspath(join(dirname(__file__), '../../staticfiles'))+'/img/bb.png',
                'codigo_linha_digitavel':num_codigo_linha_digitavel,
                'codigo_barra':codigo_barra
            }

    return emitir_documento("modelo-gru-cobranca.odt",dados)
    return gerar_pdf(request,'system/gru-cobranca.html',dados,num_codigo_linha_digitavel+'.pdf')

@permission_required('system.relatorio_pagas_vencidas', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_parcelas_pagas_vencidas(request):
    parcelas = []
    titulo = ''
    total = Decimal(0.0)
    descricao = 'Estimativas - Base de dados SisterLeg: Abril/2015'
    if request.method == "POST":
        escolha = request.POST['ordenacao']
        if escolha == 'pagas':
            titulo = 'PARCELAS PAGAS'
            descricao = 'Base de dados SisterLeg: Abril/2015'
            lista = ParcelaGuia.objects.filter( status_pagamento = True )
            for l in lista:
                total += l.parcela.valor_total
                parcelas.append( l.parcela )
        else:
            titulo = 'PARCELAS VENCIDAS'
            descricao = 'Estimativas, sem cálculo de juros, multa e correções. - Base de dados SisterLeg: Abril/2015'
            lista = Parcela.objects.all()
            for l in lista:
                if l.data_vencimento < datetime.datetime.now().date():
                    if not ParcelaGuia.objects.filter( parcela__id = l.id, status_pagamento = True ):
                        total += Decimal(l.valor_total)
                        parcelas.append( l )
        print escolha
    return render_to_response('system/relatorio/parcelas_pagas_vencidas.html',{'titulo':titulo,'total':total,'descricao':descricao,'parcelas':parcelas}, context_instance = RequestContext(request))


@permission_required('system.importacao_arquivo_retorno', login_url='/excecoes/permissao_negada/', raise_exception=True)
def arquivo_retorno(request):
    if request.method == 'POST' and request.FILES:
        path = abspath(join(dirname(__file__), '../../media'))+'/tmp/arquivo_retorno.ref'
        res = upload_file(request.FILES['arquivo'],path,request.FILES['arquivo'].name,'ref')
        if res == '0':
            messages.add_message(request,messages.ERROR,'Erro no upload. Tente novamente.')
        elif res == '2':
            messages.add_message(request,messages.WARNING,'Arquivo com extensão incorreta.')
        elif res == '1':
            return_file_ref( reader_csv(path, ' ') )
    return render_to_response('system/arquivo_retorno.html',{}, context_instance = RequestContext(request))
