from django.db import models
from django.core.validators import MinValueValidator
from builder.models import TemplateComponent
from builder.models import Pattern
from django.template.loader import render_to_string
from pagination.paginator import *
from django.apps import apps

class Pagination(Pattern):
	name = 'pagination'
	title = models.CharField(max_length = 50)
	nItemsOnPage = models.IntegerField(default = 3, validators = [MinValueValidator(1)])
	content = models.CharField(max_length = 50)
	
	def render(self):
		paginator = TUIsDPaginator(self.get_model_elems(), self.nItemsOnPage)
		return render_to_string('patrones/pagination/view.html',
							    {"pagination": self,
							     "paginator" : paginator,
							     "page_range" : range(paginator.num_pages)
							     })
							     
	def render_config_modal(self, request):
		from .forms import PaginationForm
		form = PaginationForm(instance = self)
		print('config modal pagination')
		return render_to_string(template_name = 'pagination/configurar-modal.html',
								context = {'form' : form},
								request = request
								)
		
	def render_card(self):
		return render_to_string('patrones/pagination/build.html', {"pattern": self})
		
	def __str__(self):
		return "Paginator '"+str(self.title)+"' for table <"+str(self.content)+">"
		
	def get_model_elems(self):
		all_models = apps.get_models()
		for model in all_models:
			if(hasattr(model, 'name') and type(model.name) == str and model.name == self.content):
				return model.objects.all()
		
		print("NO se encontro el modelo Dx")
		return None


