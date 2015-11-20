from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from project.system.models import Orgao
from project.core.forms import OrgaoForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse as r
from project.core.admin import verificar_permissao_grupo
from django.http.response import HttpResponse
from project.core.relatorio_base import relatorio_pdf_base_header,\
    relatorio_pdf_base_header_title, relatorio_pdf_base,\
    relatorio_ods_base_header, relatorio_ods_base, relatorio_csv_base
from odslib import ODS

nome_relatorio      = "relatorio_orgao"
response_consulta  = "/core/orgao/consulta/"
titulo_relatorio    = "Relatorio Orgao"
planilha_relatorio  = "Regionais"


@permission_required('core.orgao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nome']
        lista = Orgao.objects.filter( nome__icontains=nome )
    else:
        lista = Orgao.objects.all()
    lista = lista.order_by( 'id' )

    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_orgao'] = lista
    return render_to_response( 'core/orgao/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))
    
@permission_required('core.orgao_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):

    '''
    if request.method == "POST":
        form = OrgaoForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render_to_response('core/orgao/cadastro.html',{'form':form},context_instance = RequestContext(request))
    return render_to_response('core/orgao/cadastro.html',{'form':OrgaoForm()},context_instance = RequestContext(request))
    '''
    
    if request.method == "POST":
        next = request.GET.get('next', '/')
        f_grupo = Orgao(
            nome = request.POST['nome'],
            ug = request.POST['ug'],
            codigo_receita = request.POST['codigo_receita'],
            descricao = request.POST['descricao']
        )
        f_grupo.save()
        if next == "/":
            return HttpResponseRedirect(r('core:orgao_consulta'))
        else:    
            return HttpResponseRedirect( next ) 
    return render_to_response('core/orgao/cadastro.html',{}, context_instance = RequestContext(request))
    
    
@permission_required('core.orgao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):

    instance = get_object_or_404(Orgao, id=id)
    if request.method == "POST":

        if not request.user.has_perm('core.orgao_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/') 

        f_orgao = Orgao(
            id = instance.id,
            nome = request.POST['nome'],
            ug = request.POST['ug'],
            codigo_receita = request.POST['codigo_receita'],
            descricao = request.POST['descricao']
        )
        f_orgao.save()
        
        return HttpResponseRedirect( r('core:orgao_consulta') )

    return render_to_response('core/orgao/edicao.html', {"objeto":instance}, context_instance = RequestContext(request))


@permission_required('sicop.orgao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_pdf(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(mimetype='application/pdf')
        doc = relatorio_pdf_base_header(response, nome_relatorio)   
        elements=[]
        
        dados = relatorio_pdf_base_header_title(titulo_relatorio)
        dados.append( ('NOME','ESTADO') )
        for obj in lista:
            dados.append( ( obj.nmorgao , obj.tbuf.nmuf ) )
        return relatorio_pdf_base(response, doc, elements, dados)
    else:
        return HttpResponseRedirect(response_consulta)

@permission_required('sicop.orgao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_ods(request):

    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    
    if lista:
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, ods)
        
        # subtitle
        sheet.getCell(0, 1).setAlignHorizontal('center').stringValue( 'Nome' ).setFontSize('14pt')
        sheet.getCell(1, 1).setAlignHorizontal('center').stringValue( 'Estado' ).setFontSize('14pt')
        sheet.getRow(1).setHeight('20pt')
        
    #TRECHO PERSONALIZADO DE CADA CONSULTA
        #DADOS
        x = 0
        for obj in lista:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.nmorgao)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.tbuf.nmuf)    
            x += 1
        
    #TRECHO PERSONALIZADO DE CADA CONSULTA     
       
        relatorio_ods_base(ods, planilha_relatorio)
        # generating response
        response = HttpResponse(mimetype=ods.mimetype.toString())
        response['Content-Disposition'] = 'attachment; filename='+nome_relatorio+'.ods'
        ods.save(response)
    
        return response
    else:
        return HttpResponseRedirect( response_consulta )

@permission_required('sicop.orgao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_csv(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(content_type='text/csv')     
        writer = relatorio_csv_base(response, nome_relatorio)
        writer.writerow(['Nome', 'Estado'])
        for obj in lista:
            writer.writerow([obj.nmorgao, obj.tbuf.nmuf])
        return response
    else:
        return HttpResponseRedirect( response_consulta )



def validacao(request_form):
    warning = True
    if request_form.POST['nome'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome da orgao')
        warning = False
    if request_form.POST['uf'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o UF')
        warning = False
    return warning