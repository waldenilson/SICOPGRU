# -- coding: utf-8 --
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from project.system.models import Tbextrato
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
from project.system.payment import iniciar_calculo, carregar_parcelas
from project.core.funcoes import gerar_codigo_barra, gerar_pdf
from project.calculation.gru import calcular_codigo_barra, calcular_linha_digitavel

@permission_required('sicop.titulo_calculo_portaria23', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):

    if request.method == "POST":
        cpf = request.POST['cpf'].replace('.','').replace('/','').replace('-','')

        if cpf != '00000000000':    
            dados = consultar(cpf)

            if dados != None:
                print 'Encontrou registro'
                if dados['dados'] == 'local':
                    lista_parcela = carregar_parcelas( dados )
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
        
    return render_to_response('system/consulta.html',{}, context_instance = RequestContext(request))


def inicio_pagamento(request, cpf):
    dados = consultar(cpf)
    if request.method == "POST":
        data_requerimento = datetime.datetime.strptime( request.POST['data_requerimento'],'%d/%m/%Y')
        data_requerimento = data_requerimento.date()
        if data_requerimento <= datetime.datetime.now().date():
            iniciar_calculo( dados, data_requerimento, request.POST.get('nossa_escola',False), AuthUser.objects.get(pk=request.user.id) )
            return HttpResponseRedirect("/sistema/consulta/")
        else:
            messages.add_message(request, messages.WARNING, 'Data do Requerimento maior que a data de hoje.')
    return render_to_response('system/calculo_pagamento.html',{'dados':dados}, context_instance = RequestContext(request))

def parcelas_pagamento(request, cpf):
    return render_to_response('system/parcelas.html',{'dados':carregar_parcelas( cpf )}, context_instance = RequestContext(request))

def gru_pagamento(request, id):

    # id da parcela

    #VARIAVEIS DA GRU
    valor_gru = '0000000175'
    dt_vencimento = datetime.datetime.now()

    #CRIACAO DOS NUMEROS E CODIGO DE BARRA
    num_codigo_barra = calcular_codigo_barra(valor_gru, dt_vencimento)
    num_codigo_linha_digitavel = calcular_linha_digitavel(num_codigo_barra,valor_gru, dt_vencimento)
    codigo_barra = gerar_codigo_barra(num_codigo_barra)

    print 'barra: '+num_codigo_barra
    print 'linha: '+num_codigo_linha_digitavel

    #CRIACAO DA GRU PDF
    dados = {
                'icone':abspath(join(dirname(__file__), '../../staticfiles'))+'/img/bb.png',
                'codigo_linha_digitavel':num_codigo_linha_digitavel,
                'codigo_barra':codigo_barra
            }
    return gerar_pdf(request,'system/gru-cobranca.html',dados,num_codigo_linha_digitavel+'.pdf')
