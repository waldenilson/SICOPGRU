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
from django.http import HttpResponse, HttpRequest
from django.template import loader, Context
import os
from os.path import abspath, join, dirname
from django.conf import settings
from django.template.loader import get_template
from django.template import loader
from project.system.integrator import consultar
#from project.core.funcoes import gerar_codigo_barra, gerar_pdf
#from project.calculation.gru import calcular_codigo_barra, calcular_linha_digitavel


@permission_required('sicop.titulo_calculo_portaria23', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):

    p_extrato = []
    if request.method == "POST":
        cpf = request.POST['cpf'].replace('.','').replace('/','').replace('-','')
        
        if consultar(cpf) != None:
            print 'Encontrou registro'
        else:
            print 'Não encontrou registro'
        
    return render_to_response('system/consulta.html',{}, context_instance = RequestContext(request))
