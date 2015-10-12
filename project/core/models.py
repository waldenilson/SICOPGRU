# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

#from django.contrib.gis.db import models
from django.db import models

class AuthGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, unique=True)
    class Meta:
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)
    class Meta:
        db_table = 'auth_permission'

class Regional(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=80, blank=True)
    descricao = models.TextField(blank=True)
    uf = models.ForeignKey('Uf', null=True, blank=True)
    nrclasse = models.SmallIntegerField()
    class Meta:
        db_table = 'regional'

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField()
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    regional = models.ForeignKey(Regional)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        db_table = 'auth_user_user_permissions'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', null=True, blank=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    class Meta:
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    class Meta:
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=40, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = 'django_session'

class DjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)
    domain = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    class Meta:
        db_table = 'django_site'

class Municipio(models.Model):
    nome_mun_maiusculo = models.CharField(max_length=50, db_column='Nome_Mun_Maiusculo', blank=True) # Field name made lowercase.
    nome_mun = models.CharField(max_length=50, db_column='Nome_Mun', blank=True) # Field name made lowercase.
    codigo_mun = models.IntegerField(null=True, db_column='Codigo_Mun', blank=True) # Field name made lowercase.
    regiao = models.CharField(null=True, max_length=50, db_column='Regiao', blank=True) # Field name made lowercase.
    uf = models.CharField(max_length=2, db_column='UF', blank=True) # Field name made lowercase.
    sr = models.CharField(null=True, max_length=50, db_column='SR', blank=True) # Field name made lowercase.
    codigo_uf = models.ForeignKey('Uf', null=True, db_column='Codigo_UF', blank=True) # Field name made lowercase.
    populacao = models.CharField(null=True, max_length=50, db_column='Populacao', blank=True) # Field name made lowercase.
    nrmodulofiscal = models.IntegerField(null=True, blank=True)
    nrfracaominima = models.IntegerField(null=True, blank=True)
    id = models.AutoField(primary_key=True)
    vlterranua = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    class Meta:
        db_table = 'municipio'

class Uf(models.Model):
    sigla = models.CharField(max_length=2, blank=True)
    nmuf = models.CharField(max_length=50, blank=True)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'uf'


'''

class Tbdivisao(models.Model):
    nmdivisao = models.CharField(max_length=80, blank=True)
    dsdivisao = models.TextField(blank=True)
    tbuf = models.ForeignKey('Tbuf', null=True, blank=True)
    id = models.AutoField(primary_key=True)
    nrclasse = models.SmallIntegerField()
    class Meta:
        db_table = 'tbdivisao'

class Tbmunicipio(models.Model):
    nome_mun_maiusculo = models.CharField(max_length=50, db_column='Nome_Mun_Maiusculo', blank=True) # Field name made lowercase.
    nome_mun = models.CharField(max_length=50, db_column='Nome_Mun', blank=True) # Field name made lowercase.
    codigo_mun = models.IntegerField(null=True, db_column='Codigo_Mun', blank=True) # Field name made lowercase.
    regiao = models.CharField(null=True, max_length=50, db_column='Regiao', blank=True) # Field name made lowercase.
    uf = models.CharField(max_length=2, db_column='UF', blank=True) # Field name made lowercase.
    sr = models.CharField(null=True, max_length=50, db_column='SR', blank=True) # Field name made lowercase.
    codigo_uf = models.ForeignKey('Tbuf', null=True, db_column='Codigo_UF', blank=True) # Field name made lowercase.
    populacao = models.CharField(null=True, max_length=50, db_column='Populacao', blank=True) # Field name made lowercase.
    nrmodulofiscal = models.IntegerField(null=True, blank=True)
    nrfracaominima = models.IntegerField(null=True, blank=True)
    id = models.AutoField(primary_key=True)
    vlterranua = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    class Meta:
        db_table = 'tbmunicipio'

class Tbuf(models.Model):
    sigla = models.CharField(max_length=2, blank=True)
    nmuf = models.CharField(max_length=50, blank=True)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbuf'
'''