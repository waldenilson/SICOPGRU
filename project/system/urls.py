# coding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('project.system',
   url(r'^consulta-unica', 'views.consulta_unica'),
   url(r'^consulta-titulado', 'views.consulta_titulado'),
   url(r'^inicio-pagamento/(?P<cpf>\d+)/', 'views.inicio_pagamento'),
   url(r'^parcelas-pagamento/(?P<cpf>\d+)/', 'views.parcelas_pagamento'),
   url(r'^gru-pagamento/(?P<id>\d+)/', 'views.gru_pagamento'),
   url(r'^arquivo-retorno', 'views.arquivo_retorno'),

   url(r'^relatorio/parcelas/pagas-vencidas/', 'views.relatorio_parcelas_pagas_vencidas'),
      

   url(r'^emissao/(?P<id>\d+)/', 'views.emissao'),
   url(r'^processo/digitar/', 'views.digitar'),
   url(r'^gerar_boleto/(?P<id>\d+)/', 'views.gerar_boleto_pagamento'),

   url(r'^tr_mensal/consulta/', 'tr_mensal.consulta'),
   url(r'^tr_mensal/cadastro/', 'tr_mensal.cadastro'),
   url(r'^tr_mensal/edicao/(?P<id>\d+)/', 'tr_mensal.edicao'),

   )
