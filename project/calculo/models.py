# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

'''
class Tbcalculotitulo(models.Model):
    tbextrato = models.ForeignKey('Tbextrato',blank=True)
    parcela = models.IntegerField()
    cdrecolhimento = models.CharField(blank=True,max_length=20)
    nrreferencia = models.CharField(blank=True,max_length=20)
    dtvencimento = models.DateField()
    cdug = models.CharField(blank=True,max_length=20)
    vlprincipal = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    vldesconto = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    vldeducoes = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    vlcorrecao = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    vlmulta = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    vljuros = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    vlacrescimos = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    vltotal = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    auth_user = models.ForeignKey('core.AuthUser')
    stpaga  = models.BooleanField(default=False)
    stgerada  = models.BooleanField(default=False)
    dtentrega = models.DateField(null=True)
    dtrequerimento = models.DateField(null=True)
    dtgeracao = models.DateField(null=True)
    dtpagamento = models.DateField(null=True)

    
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbcalculotitulo'

class TbtrMensal(models.Model):
    id = models.AutoField(primary_key=True)
    valor = models.FloatField()
    mes = models.IntegerField()
    ano = models.IntegerField()
    class Meta:
        db_table = 'tbtr_mensal'

class Tbextrato(models.Model):
    id_req = models.TextField(blank=True) #n
    cpf_req = models.TextField(blank=True)
    origem = models.TextField(blank=True)
    dap = models.TextField(blank=True) #n
    nome_req = models.TextField(blank=True)
    apelido_req = models.TextField(blank=True)
    cooperativa_req = models.TextField(blank=True) #n
    nome_mae_req = models.TextField(blank=True) #n
    doc_id_req = models.TextField(blank=True) #n
    tipo_doc_id_req = models.TextField(blank=True) #n
    orgao_emiss_doc_id_req = models.TextField(blank=True) #n
    data_nasc_req = models.DateField(null=True, blank=True)
    nacionalidade_req = models.TextField(blank=True)
    naturalidade_req = models.TextField(blank=True) #n
    sexo_req = models.TextField(blank=True)
    estado_civil_req = models.TextField(blank=True)
    endereco_req = models.TextField(blank=True)
    telefone_req = models.TextField(blank=True)
    cpf_conj = models.TextField(blank=True)
    nome_conj = models.TextField(blank=True)
    nome_mae_conj = models.TextField(blank=True)
    doc_id_conj = models.TextField(blank=True) #n
    tipo_doc_id_conj = models.TextField(blank=True) #n
    orgao_emiss_doc_id_conj = models.TextField(blank=True) #n
    data_nasc_conj = models.DateField(null=True, blank=True)
    nacionalidade_conj = models.TextField(blank=True)
    estado_civil_conj = models.TextField(blank=True)
    sexo_conj = models.TextField(blank=True)
    naturalidade_conj = models.TextField(blank=True) #n
    numero_processo = models.TextField(blank=True)
    sncr = models.TextField(blank=True)
    nome_imovel = models.TextField(blank=True) #n
    atividade_economica = models.TextField(blank=True)
    data_ocupacao_originaria = models.DateField(null=True, blank=True) #n
    data_ocupacao_atual = models.DateField(null=True, blank=True) #n
    ocupante_primitivo = models.TextField(blank=True) #n
    posse_mansa_pacifica = models.TextField(blank=True) #n
    doc_expedido_orgao_publico = models.TextField(blank=True) #n
    indicacao_acesso = models.TextField(blank=True)
    distancia_nucleo_urbano = models.TextField(blank=True) #n
    tipo_acesso = models.TextField(blank=True) #n
    nome_gleba = models.TextField(blank=True) #n
    nome_gleba_cadastro = models.TextField(blank=True) #n
    area = models.TextField(blank=True) #n
    area_medida = models.TextField(blank=True) #n
    tamanho_modulos_fiscais = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True) #n
    area_total_imovel = models.DecimalField(null=True, max_digits=10, decimal_places=4, blank=True) #n
    area_maior_fracao_minima = models.TextField(blank=True) #n
    uf_imovel = models.TextField(blank=True) #n
    cod_municipio = models.TextField(blank=True) #n
    nome_municipio = models.TextField(blank=True) #n
    situacao_processo = models.TextField(blank=True)
    data_inicio_situacao_atual = models.DateField(null=True, blank=True)
    entidade_cadastramento = models.TextField(blank=True) #n
    responsavel_cadastramento = models.TextField(blank=True) #n
    inspetor_cadastramento = models.TextField(blank=True) #n
    data_cadastro = models.DateField(null=True, blank=True)
    inspetor_transmissao = models.TextField(blank=True) #n
    data_transmissao = models.DateField(null=True, blank=True)
    numero_assentimento = models.CharField(max_length=50, blank=True)
    ano_assentimento = models.DecimalField(null=True, max_digits=4, decimal_places=0, blank=True)
    valor_imovel = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    data_vencimento_primeira_prestacao = models.DateField(null=True, blank=True)
    data_inicio_etapa_anterior = models.DateField(null=True, blank=True) #n
    id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = 'tbextrato'
'''


#SCHEMA ADMINISTRACAO

class Orgao(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=80)
    descricao = models.TextField(blank=True,null=True)
    codigo_receita = models.CharField(max_length=20)
    ug = models.CharField(max_length=20)
    class Meta:
        db_table = 'administracao.orgao'

class Convenio(models.Model):
    id = models.AutoField(primary_key=True)
    orgao = models.ForeignKey(Orgao,null=False,primary_key=True)
    numero = models.CharField(max_length=80)
    descricao = models.TextField(blank=True,null=True)
    instituicao_financeira = models.CharField(max_length=80)
    class Meta:
        db_table = 'administracao.convenio'


#SCHEMA TITULACAO

class Imovel(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=80)
    sncr = models.CharField(max_length=20)
    gleba = models.CharField(max_length=80)
    area_total = models.DecimalField(null=True, max_digits=10, decimal_places=4, blank=True) #n
    tamanho_modulo_fiscal = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True) #n
    municipio = models.ForeignKey('core.Municipio',null=False,primary_key=True)
    Regional = models.ForeignKey('core.Regional',null=False,primary_key=True)
    class Meta:
        db_table = 'titulacao.imovel'


class ImovelTitulo(models.Model):
    id = models.AutoField(primary_key=True)
    imovel = models.ForeignKey(Imovel,null=False,primary_key=True)
    titulo = models.ForeignKey(Titulo,null=False,primary_key=True)
    valor_imovel = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    class Meta:
        db_table = 'titulacao.imovel_titulo'

class HistoricoImovel(models.Model):
    id = models.AutoField(primary_key=True)
    imovel_titulo = models.ForeignKey(ImovelTitulo,null=False,primary_key=True)
    descricao = models.TextField(blank=True,null=True)
    data_hora = models.DateTimeField()
    auth_user = models.ForeignKey('core.AuthUser',null=False)
    class Meta:
        db_table = 'titulacao.historico_imovel'

class Titulo(models.Model):
    id = models.AutoField(primary_key=True)
    numero = models.CharField(max_length=20)
    tipo = models.CharField(max_length=20)
    processo = models.CharField(max_length=20)
    nome_titulado = models.CharField(max_length=80)
    cpf_titulado = models.CharField(max_length=20)
    data_emissao = models.DateTimeField()
    class Meta:
        db_table = 'titulacao.titulo'


#SCHEMA PAGAMENTO

class FormaPagamento(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=80)
    descricao = models.TextField(blank=True,null=True)
    class Meta:
        db_table = 'pagamento.forma_pagamento'

class Pagamento(models.Model):
    id = models.AutoField(primary_key=True)
    imovel_titulo = models.ForeignKey(ImovelTitulo,null=False,primary_key=True)
    convenio = models.ForeignKey(Convenio,null=False,primary_key=True)
    data_requerimento = models.DateField()
    nossa_escola = models.BooleanField(default=False)
    forma_pagamento = models.ForeignKey(FormaPagamento)
    created_at = models.DateTimeField(auto_now_add=True)
    auth_user_creator = models.ForeignKey('core.AuthUser')
    updated_at = models.DateTimeField()
    auth_user_updater = models.ForeignKey('core.AuthUser')
    class Meta:
        db_table = 'pagamento.pagamento'

class Parcela(models.Model):
    id = AutoField(primary_key=True)
    pagamento = models.ForeignKey(Pagamento,null=False,primary_key=True)
    numero = models.IntegerField(null=False)
    data_vencimento = models.DateField()
    valor_principal = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    valor_deducao = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    valor_multa = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    valor_juro = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    valor_acrescimo = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    valor_correcao = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    class Meta:
        db_table = 'pagamento.parcela'


class ParcelaGuia(models.Model):
    id = AutoField(primary_key=True)
    parcela = models.ForeignKey(Pagamento,null=False,primary_key=True)
    guia = models.ForeignKey(Pagamento,null=False,primary_key=True)
    data_pagamento = models.DateTimeField()
    status_pagamento = models.BooleanField(default=False)
    class Meta:
        db_table = 'pagamento.parcela_guia'

class Guia(models.Model):
    id = models.AutoField(primary_key=True)
    id_convenio = models.IntegerField()#primary_key
    numero_via = models.IntegerField(null=False)
    codigo_barra = models.TextField()
    codigo_linha_digitavel = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    codigo_retorno = models.TextField()
    class Meta:
        db_table = 'pagamento.guia'
