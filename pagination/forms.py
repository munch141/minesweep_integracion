from django.forms import ModelForm, widgets
from django.forms.models import inlineformset_factory
from .models import Pagination
import django.apps

aux = django.apps.apps.get_models()
cont_choices = []
for elem in aux:
	if(hasattr(elem, 'name') and type(elem.name) == str):
		cont_choices.append((elem.name, elem.name))

class PaginationForm(ModelForm):
	class Meta:
		model = Pagination
		fields = ['title', 'nItemsOnPage', 'content']
		labels = {
			'title' : 'Titulo',
			'nItemsOnPage' : 'Numero de elementos por pagina',
			'content' : 'Contenido a mostrar'
		}
		widgets = {
			'content' : widgets.Select(choices = cont_choices)
		}
