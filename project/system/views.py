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
from project.system.integrator import consultar
from project.system.payment import iniciar_calculo, carregar_parcelas
#from project.core.funcoes import gerar_codigo_barra, gerar_pdf
#from project.calculation.gru import calcular_codigo_barra, calcular_linha_digitavel

@permission_required('sicop.titulo_calculo_portaria23', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):

    if request.method == "POST":
        cpf = request.POST['cpf'].replace('.','').replace('/','').replace('-','')
        
        dados = consultar(cpf)

        if dados != None:
            print 'Encontrou registro'
            if dados['situacao'] == 'Titulado':
                if dados['dados'] == 'local':
                    print 'carregar a(s) parcela(s) do pagamento.'
                    lista_parcela = carregar_parcelas( dados )
                elif dados['dados'] == 'externa':
                    if dados['modulo_fiscal'] >= 1.0:
                        return render_to_response('system/calculo_pagamento.html',{'dados':dados}, context_instance = RequestContext(request))
                        #iniciar_calculo( dados )
                    else:
                        messages.add_message(request, messages.WARNING, 'Título isento de pagamento. Abaixo de 1 módulo fiscal.')                    
            else:
                messages.add_message(request, messages.WARNING, 'Requerente não titulado.')
        else:
            messages.add_message(request, messages.WARNING, 'Não encontrado registro.')
        
    return render_to_response('system/consulta.html',{}, context_instance = RequestContext(request))


def inicio_pagamento(request, cpf):
    if request.method == "POST":
        iniciar_calculo( consultar(cpf), request.POST['data_requerimento'], request.POST.get('nossa_escola',False) )
        return HttpResponseRedirect("/sistema/consulta/")
    return render_to_response('system/consulta.html',{}, context_instance = RequestContext(request))
