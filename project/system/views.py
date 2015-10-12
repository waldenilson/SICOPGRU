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
from project.core.funcoes import gerar_codigo_barra, gerar_pdf
from project.calculation.gru import calcular_codigo_barra, calcular_linha_digitavel

nome_relatorio      = "relatorio_portaria80"
response_consulta  = "/core/restrito/portaria80/calculo/"
titulo_relatorio    = "Calculo Portaria 80 - Clausulas Resolutivas"

global juros
global principal_corrigido

@permission_required('sicop.titulo_calculo_portaria23', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):

    p_extrato = []
    if request.method == "POST":
        numero = request.POST['numero'].replace('.','').replace('/','').replace('-','')
        cpf = request.POST['cpf'].replace('.','').replace('/','').replace('-','')
        requerente = request.POST['requerente']
        titulo = request.POST['cdtitulo']
        p_extrato = []
        #p_extrato = Tbextrato.objects.all().filter(numero_processo__icontains = numero,cpf_req__icontains = cpf,
        #                        nome_req__icontains = requerente, id_req__icontains = titulo,  situacao_processo__icontains = 'Titulado')
        
        #gravando na sessao o resultado da consulta preparando para o relatorio/pdf'''
        #exibir uma warning informando que o campo data do requerimento deve ser preenchido
       

    return render_to_response('system/consulta.html',{'lista':p_extrato}, context_instance = RequestContext(request))
