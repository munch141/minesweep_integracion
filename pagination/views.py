import json
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import get_template
from builder.models import Template, TemplateComponent
from .forms import PaginationForm
from .models import Pagination

def get_tempid_pos(request):
	#if request.method == 'GET':
	#	return request.GET.get("template", None), request.GET.get("position", None)
	#elif request.method == 'POST':
	return request.POST.get("template", None), request.POST.get("position", None)
		
def get_last_pos(template_id):
	template = Template.objects.get(pk = int(template_id))
	patterns = template.sorted_patterns()
	
	if patterns == []:
		position = 0
	else:
		position = patterns[-1].template_component.get().position
		position += 1
		
	return position
	
def pagination_config(request):
	# Creo mi objeto Pagination
	pagination = Pagination()
		
	# En caso de estar creando patron decido en que posicion ponerlo
	
	
	# Mostrar formulario de creacion/modificacion
	if request.method == 'GET':
		form = PaginationForm(instance = pagination)
		
		return render(request, 'pagination/configurar-modal.html', {'form': form, 'pagination' : pagination})
	# Procesar formulario
	elif request.method == 'POST':
		# Obtengo template_id y position de mi request
		template_id = request.POST.get("template", None)
		position = get_last_pos(template_id)
		
		form = PaginationForm(request.POST, instance = pagination)
		if form.is_valid():
			new_pagination = form.save()
			TemplateComponent.objects.create(content_object = new_pagination, template_id = int(template_id), position = int(position))
			
			return render(request, 'pagination/pagination_create_success.html', {'pagination': pagination, 'position': position})
	
	return render(request, '', {})

def pagination_delete(request):
	template = request.GET.get('template', None)
	position = request.GET.get('position', None)

	component = TemplateComponent.objects.filter(position=int(position), template_id=int(template))
	pagination = Pagination.objects.get(template_component=component)
	pagination.delete()

	return JsonResponse(data={})
	
def pagination_update(request, pk):
	pagination = Pagination.objects.get(pk = pk)
	
	if request.method == 'GET':
		form = PaginationForm(instance = pagination)
		
		return render(request, 'pagination/pagination_form.html', {'form': form, 'pagination' : pagination})
	elif request.method == 'POST':
		form = PaginationForm(request.POST, instance = pagination)
		if form.is_valid():
			pagination.title = form.cleaned_data['title']
			pagination.nItemsOnPage = form.cleaned_data['nItemsOnPage']
			pagination.content = form.cleaned_data['content']
			pagination.save()
			component = TemplateComponent.objects.filter(content_object = pagination)
			
			return render(request, 'pagination/pagination_create_success.html', {'pagination': pagination, 'position': component.position})
