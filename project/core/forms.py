# formularios customizados
from django.forms import models
from django import forms
from project.core.models import AuthGroup, Tbdivisao, Tbmunicipio

class FormDivisao(models.ModelForm):
    class Meta:
        model = Tbdivisao
                
class FormAuthGroup(models.ModelForm):
    class Meta:
        model = AuthGroup

class FormMunicipio(models.ModelForm):
    class Meta:
        model = Tbmunicipio        