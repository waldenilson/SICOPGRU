
# -*- coding: UTF-8 -*-

from django.contrib import admin
from project.core.models import AuthUser, AuthUserGroups, AuthGroupPermissions
from django.http.response import HttpResponse
import csv
import sqlite3
from datetime import datetime
from django.core import serializers
import urllib2
import json

def verificar_permissao_grupo(usuario, grupos):
    if usuario:
        permissao = False
        obj_usuarios = AuthUserGroups.objects.filter( user = usuario.id )
        for obj in obj_usuarios:
            for obj_g in grupos:
                if obj.user.id == usuario.id and obj.group.name == str(obj_g):
                    permissao = True
        return permissao
    return False

def verificar_permissoes(grupo, permissoes):
    if grupo:
        permissao = False
        obj_grupos = AuthGroupPermissions.objects.filter( group = grupo.id )
        for obj in obj_grupos:
            for obj_g in permissoes:
                if obj.group.id == grupo.id and obj.permission.id == obj_g.id:
                    permissao = True
        return permissao
    return False

def mes_do_ano_texto(inteiro):
    mes_texto = ""
    
    if inteiro == 1: mes_texto = "Janeiro"
    elif inteiro == 2: mes_texto = "Fevereiro"
    elif inteiro == 3: mes_texto = "Marco"
    elif inteiro == 4: mes_texto = "Abril"
    elif inteiro == 5: mes_texto = "Maio"
    elif inteiro == 6: mes_texto = "Junho"
    elif inteiro == 7: mes_texto = "Julho"
    elif inteiro == 8: mes_texto = "Agosto"
    elif inteiro == 9: mes_texto = "Setembro"
    elif inteiro == 10: mes_texto = "Outubro"
    elif inteiro == 11: mes_texto = "Novembro"
    elif inteiro == 12: mes_texto = "Dezembro"
    
    return mes_texto

def diferenca_mes(d2, d1):
    delta = 1
    print str(d1.month) + '/' + str(d1.year) 
    while True:
        mdays = monthrange(d1.year, d1.month)[1]
        d1 += timedelta(days=mdays)
        if d1 <= d2:
            print str(d1.month) + '/' + str(d1.year)
            delta += 1
        else:
            break
    return delta

'''
def import_tr(csv_):
    trs = []
    aux = []
    with open(csv_, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            aux.append(row)

    lines = []
    for l in aux:
        #lines.append(l[0])
        sp = l[0].split('|')
        
    #        print "ano "+sp[0] + ", mes "+str(1)+", valor "+sp[1]
        if sp[12] == '-':
            obj = TbtrMensal( ano = sp[0], mes = 12, valor = None )
        else:    
            obj = TbtrMensal( ano = sp[0], mes = 12, valor = sp[12].replace(',','.') )
        obj.save()

                #obj = TbtrMensal(
                #        ano = sp[0],
                #        mes = x,
                #        valor = s
                #    )
                #obj.save()
        


    print len(lines)
    print lines
'''
#admin.site.register(AuthUser)

