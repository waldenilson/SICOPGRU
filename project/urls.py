# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf.urls import patterns, url, include
admin.autodiscover()
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
project = 'project'

handler404 = project+'.core.views_excecoes.pagina_nao_encontrada'
handler403 = project+'.core.views_excecoes.permissao_negada'
handler500 = project+'.core.views_excecoes.erro_servidor'


urlpatterns = patterns('',

    # DAJAXICE AJAX DO PROJETO
    #url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
#    url(r'^livro/',include(project+'.livro.urls',namespace='livro')),
#    url(r'^servidor/',include(project+'.servidor.urls',namespace='servidor')),
#    url(r'^documento/',include(project+'.documento.urls',namespace='documento')),
#    url(r'^web/',include(project+'.web.urls',namespace='web')),
    url(r'^sistema/',include(project+'.system.urls',namespace='sistema')),
    url(r'^core/',include(project+'.core.urls',namespace='core')),


    # ACESSO AO PUBLICO
    url(r'^$', project+'.web.views_publicas.inicio'),
    url(r'^web/equipe/', project+'.web.views_publicas.equipe'),
    url(r'^media/(?P<path>.*)$',project+'.core.util.media.download', {'document_root': settings.MEDIA_ROOT}),
   
    # GEOINFORMACOES
#    url(r'^geo/glebas_federais/', project+'.tramitacao.restrito.geoinformacao.glebas_federais'),
#    url(r'^geo/openlayers/', project+'.tramitacao.restrito.geoinformacao.openlayers'),
    
    #INIT------------------------------SICOP---------------------------------------------------------------------------------

    # ACESSO RESTRITO SICOP PROCESSO
            
   # ACESSO RESTRITO REGIONAL
    url(r'^core/regional/consulta/', 'project.core.restrito.regional.consulta'),
    url(r'^core/regional/cadastro/', 'project.core.restrito.regional.cadastro'),
    url(r'^core/regional/edicao/(?P<id>\d+)/', 'project.core.restrito.regional.edicao'),
    url(r'^core/regional/relatorio/pdf/', 'project.core.restrito.regional.relatorio_pdf'),
    url(r'^core/regional/relatorio/ods/', 'project.core.restrito.regional.relatorio_ods'),
    url(r'^core/regional/relatorio/csv/', 'project.core.restrito.regional.relatorio_csv'),
  
  # ACESSO RESTRITO SICOP GRUPO
    url(r'^core/grupo/consulta/', 'project.core.restrito.grupo.consulta'),
    url(r'^core/grupo/cadastro/', 'project.core.restrito.grupo.cadastro'),
    url(r'^core/grupo/edicao/(?P<id>\d+)/', 'project.core.restrito.grupo.edicao'),
    url(r'^core/grupo/relatorio/pdf/', 'project.core.restrito.grupo.relatorio_pdf'),
    url(r'^core/grupo/relatorio/ods/', 'project.core.restrito.grupo.relatorio_ods'),
    url(r'^core/grupo/relatorio/csv/', 'project.core.restrito.grupo.relatorio_csv'),

  # ACESSO RESTRITO SICOP PERMISSAO
    url(r'^core/permissao/consulta/', 'project.core.restrito.permissao.consulta'),
    url(r'^core/permissao/cadastro/', 'project.core.restrito.permissao.cadastro'),
    url(r'^core/permissao/edicao/(?P<id>\d+)/', 'project.core.restrito.permissao.edicao'),
    url(r'^core/permissao/relatorio/pdf/', 'project.core.restrito.permissao.relatorio_pdf'),
    url(r'^core/permissao/relatorio/ods/', 'project.core.restrito.permissao.relatorio_ods'),
    url(r'^core/permissao/relatorio/csv/', 'project.core.restrito.permissao.relatorio_csv'),

  # ACESSO RESTRITO SICOP USUARIO
    url(r'^core/usuario/consulta/', 'project.core.restrito.usuario.consulta'),
    url(r'^core/usuario/cadastro/', 'project.core.restrito.usuario.cadastro'),
    url(r'^core/usuario/edicao/(?P<id>\d+)/', 'project.core.restrito.usuario.edicao'),
    url(r'^core/usuario/edicao/usuario/(?P<id>\d+)/', 'project.core.restrito.usuario.edicao_usuario_logado'),
    url(r'^core/usuario/relatorio/pdf/', 'project.core.restrito.usuario.relatorio_pdf'),
    url(r'^core/usuario/relatorio/ods/', 'project.core.restrito.usuario.relatorio_ods'),
    url(r'^core/usuario/relatorio/csv/', 'project.core.restrito.usuario.relatorio_csv'),

    # ACESSO RESTRITO SICOP MUNICIPIO
    
    url(r'^core/municipio/consulta/', 'project.core.restrito.municipio.consulta'),
    url(r'^core/municipio/edicao/(?P<id>\d+)/', 'project.core.restrito.municipio.edicao'),
        
    # CONTROLE AUTENTICACAO
    url(r'^login/', 'django.contrib.auth.views.login', {"template_name":"index.html"}),
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login', {"login_url":"/"}),
    url(r'^core/admin/', include(admin.site.urls)),
    
)

