# Create your views here.
from django.template import loader
from django.http.response import HttpResponse
from django.template.context import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from reportlab.pdfgen import canvas
from django.utils.datetime_safe import date
from reportlab.platypus.flowables import Spacer
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Image
import time
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
import urllib2
import json
import pprint
from project.core.models import AuthUser, Regional
from project.core.funcoes import verificaDivisaoUsuario
   
def inicio(request):
    if request.user.id is not None:
        # gravando na sessao a divisao do usuario logado
        request.session['regional'] = AuthUser.objects.get( pk = request.user.id ).regional.nome +" - "+AuthUser.objects.get( pk = request.user.id ).regional.uf.nmuf
        verificaDivisaoUsuario(request) 
    return render(request, "index.html")

def equipe(request):
	return render_to_response('equipe.html',{},context_instance = RequestContext(request))   

def organizacao(request):        
    return render(request, "organizacao.html")

def mobile(request):        
    return render(request, "mobile.html")
    
