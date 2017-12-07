from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Pregunta, Opcion
from django.urls import reverse
from django.forms import formset_factory
from .forms import *



def index(request):
    latest_question_list = Pregunta.objects.order_by('-fecha_publ')[:7]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'encuestas/index.html', context)


def new(request):
    FormSetOpcion = formset_factory(OpcionForm, extra=2)

    if request.method == 'POST':
        form_p = PreguntaForm(request.POST)
        formset_o = FormSetOpcion(request.POST)
        if form_p.is_valid() and formset_o.is_valid():
            question = form_p.save()
            for opcion in formset_o:
                opcion = opcion.save(commit=False)
                opcion.pregunta = get_object_or_404(Pregunta, pk=question.pk)
                opcion.save()
            return redirect('encuestas:detail', question.pk)
    else:
        form_p = PreguntaForm()
        formset_o = FormSetOpcion()
    return render(request, 'encuestas/new.html', {'form_p': form_p, 'form_o': formset_o})

def detail(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    return render(request, 'encuestas/detail.html', {'pregunta': pregunta})


def results(request, pregunta_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % pregunta_id)


def vote(request, pregunta_id):
    question = get_object_or_404(Pregunta, pk=pregunta_id)
    try:
        selected_choice = question.opcion_set.get(pk=request.POST['choice'])
    except (KeyError, Opcion.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'encuestas/detail.html', {
            'pregunta': question,
            'error_message': "Ninguna opción fue seleccionada",
        })
    else:
        selected_choice.votos += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('encuestas:results', args=(question.id,)))


def results(request, pregunta_id):
    question = get_object_or_404(Pregunta, pk=pregunta_id)
    return render(request, 'encuestas/results.html', {'pregunta': question})