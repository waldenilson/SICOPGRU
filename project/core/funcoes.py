# -- coding: utf-8 --
from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext, Context

from django.http.response import HttpResponseRedirect, HttpResponse
from project.core.models import AuthUser,AuthUserGroups, Regional
from types import InstanceType
from project.core.admin import verificar_permissao_grupo
import datetime
from django.contrib import messages
from django.utils import simplejson
from project.core.relatorio_base import relatorio_csv_base, relatorio_ods_base,\
    relatorio_ods_base_header, relatorio_pdf_base,\
    relatorio_pdf_base_header_title, relatorio_pdf_base_header
from django.contrib.auth.models import Permission
from django import http
from django.template.loader import get_template
from django.template import Context

#import ho.pisa as pisa
import cStringIO as StringIO
import os
from django.conf import settings
from project import settings as configuracao
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.template import loader
from project.calculation.barcode import codigodebarra
import urllib2

def formatDataToText( formato_data ):
    if formato_data:
        if len(str(formato_data.day)) < 2:
            dtaberturaprocesso = '0'+str(formato_data.day)+"/"
        else:
            dtaberturaprocesso = str(formato_data.day)+"/"
        if len(str(formato_data.month)) < 2:
            dtaberturaprocesso += '0'+str(formato_data.month)+"/"
        else:
            dtaberturaprocesso += str(formato_data.month)+"/"
        dtaberturaprocesso += str(formato_data.year)
        return str( dtaberturaprocesso )
    else:
        return "";

def verificaDivisaoUsuario(request):
    classe_divisao = AuthUser.objects.get( pk = request.user.id ).regional.nrclasse
    divisoes = []
    id_divisoes = []
    id_uf_classe = []
    
    if Regional.objects.filter(nrclasse__lt = classe_divisao ):
        #a divisao do usuario logado permite que veja objetos de sua div e das divs de classes menores que a sua
        request.session['isdivisao'] = False
        p_divisoes = Regional.objects.filter(nrclasse__lte = classe_divisao )
        for obj in p_divisoes:
            divisoes.append(obj)
    else:
        #eh uma divisao regional e/ou possui a menor classe da hierarquia
        request.session['isdivisao'] = True
        #usa a divisao do usuario logado
        divisoes = Regional.objects.all().filter(id = AuthUser.objects.get(pk = request.user.id ).regional.id)
    
    for obj in divisoes:
        id_divisoes.append(obj.id)#cria lista com as divisoes que o usuario pode acessar
    for obj in divisoes:
        id_uf_classe.append(obj.uf.id)#cria lista com os estados que o usuario pode acessar
    request.session['divisoes'] = id_divisoes
    request.session['uf'] = id_uf_classe
    request.session['classe'] = [1,2,3,4,5,6,7,8,9,10]

def gerar_pdf(request, template_path, data, name):
    
    # Render html content through html template with context
    t = loader.get_template(template_path)
    c = Context(data)
    html =  t.render(c)
    file = open(os.path.join(configuracao.MEDIA_ROOT+'/tmp/gru', name), "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=file)
    file.seek(0)
    pdf = file.read()
    file.close()            # Don't forget to close the file handle
    return HttpResponse(pdf, mimetype='application/pdf')

# Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
def link_callback(uri, rel):
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                    'media URI must start with %s or %s' % \
                    (sUrl, mUrl))
    return path

def gerar_codigo_barra(codigo):
    try:
        barra = codigodebarra()
        image = barra.getcodbarra(codigo)
        image.save( os.path.join(settings.MEDIA_ROOT+'/tmp/barcode/'+codigo+'.PNG' ))
        return os.path.join(settings.MEDIA_ROOT+'/tmp/barcode/'+codigo+'.PNG')
    except:
        return None

def consumir_url_json(url):
    retorno = None
    try:
        response = urllib2.urlopen( url , timeout=3)
        retorno = json.loads(response.read())
    except:
        pass
    return retorno           
