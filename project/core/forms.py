# formularios customizados
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from project.core.models import AuthGroup, Regional, Municipio
from project.system.models import Orgao

class FormRegional(forms.ModelForm):
    class Meta:
        model = Regional
                
class FormAuthGroup(forms.ModelForm):
    class Meta:
        model = AuthGroup

class FormMunicipio(forms.ModelForm):
    class Meta:
        model = Municipio      


def NomeValidator(value):
	if len(value) <= 3:
		raise ValidationError(_('Informe um nome maior que 3 letras.'))

class OrgaoForm(forms.ModelForm):
	class Meta:
		model = Orgao

	descricao = forms.CharField(
		required = False,
		widget=forms.Textarea(
				attrs={
					'cols':'1000'
				}
			)
	)

	def __init__(self,*args,**kwargs):
		super(OrgaoForm,self).__init__(*args,**kwargs)
		self.fields['nome'].validators.append(NomeValidator)
