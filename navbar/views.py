from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib import messages
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.html import escape
import json
from django.core.urlresolvers import reverse

def index(request):
    return render(request, 'navbar/index.html')


@csrf_exempt
def showCodigo(request):

	html = ''
	if request.method == 'POST':

		url = request.POST.get('location')
		lista = json.loads(url)		

		html = render_to_string('navbar/navbar.html', { 'lista': lista })

		# Se crea un codigo de navbar no responsive para mostrarlo
		# en la vista del codigo generado.
		htmlNavBar = html.replace("navbar-toggleable-md","navbar-expand")
		context = {'html':escape(html),'htmlCodigo':htmlNavBar}
		template = loader.get_template('navbar/navbarCodigo.html')
		return HttpResponse(template.render(context,request))

	context = {'html':html}
	template = loader.get_template('navbar/navbarCodigo.html')
	return HttpResponse(template.render(context,request))
		

