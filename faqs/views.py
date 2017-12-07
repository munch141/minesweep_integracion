from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.urls import reverse
from django.forms import formset_factory
from .forms import *

# Create your views here.
def index(request):
    #latest_faqs_list = Categoria.objects.order_by('-fecha_publ')[:7]
    context = {
    }
    return render(request, 'faqs/index.html', context)

def new(request):
    FormSetPreguntas = formset_factory(PreguntaForm)

    if request.method == 'POST':
        form_f = CategoriaForm(request.POST)
        formset_p = FormSetPreguntas(request.POST, form_kwargs={'empty_permitted': False})

        if form_f.is_valid() and formset_p.is_valid():
            # Revisar si el tema es vacio, no debo gurdarlo
            #faq = Faq()
            #faq.save()
            if form_f.cleaned_data['nombre'] == "":    
                for preg in formset_p:
                    preg = preg.save(commit=False)
                    #preg.faq = faq
                    preg.save()
                return redirect('faqs:detail')
            else:
                tema = form_f.save(commit=False)
                #tema.faq = faq
                tema.save()
                for preg in formset_p:
                    preg = preg.save(commit=False)
                    #preg.faq = faq
                    preg.tema = get_object_or_404(Categoria, pk=tema.pk)
                    preg.save()
                return redirect('faqs:detail')
    else:
        form_f = CategoriaForm()
        formset_p = FormSetPreguntas()
    return render(request, 'faqs/new.html', {'form_f': form_f, 'form_p': formset_p})

def detail(request):
    sin_cat = Pregunta.objects.filter(tema=None)
    categorias = Categoria.objects.all().order_by("id")
    #preg_list = faq.pregunta_set.all().order_by("id")
    return render(request, 'faqs/detail.html', {'sin_cat': sin_cat, 'categorias': categorias})