# formularios customizados
from django.forms import models
from django import forms
from project.core.models import AuthGroup, Regional, Municipio

class FormRegional(models.ModelForm):
    class Meta:
        model = Regional
                
class FormAuthGroup(models.ModelForm):
    class Meta:
        model = AuthGroup

class FormMunicipio(models.ModelForm):
    class Meta:
        model = Municipio        