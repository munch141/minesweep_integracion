import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from builder.models import *
from encuestas.models import *
from carrusel.models import Carousel, Content
from faqs.models import *
from formBuilder.models import *
from captcha_pattern.models import *
from accordion.models import Accordion
from minesweep.models import Minesweep
from builder.forms import *
from encuestas.forms import *
from carrusel.forms import *
from navbar.models import *
from django.forms import formset_factory, model_to_dict
from .forms import *
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core import serializers
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt


class buildTemplate(LoginRequiredMixin,TemplateView):
    login_url = '/login/'
    redirect_field_name = '/'
    template_name = 'builder/build.html'

    def get_context_data(self, **kwargs):
        context = super(buildTemplate, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        return render(request, '/builder/build.html')


class homeTemplate(TemplateView):
    template_name = 'home.html'


class ver_templatesTemplate(LoginRequiredMixin,TemplateView):
    login_url = '/login/'
    redirect_field_name = '/'
    template_name = 'ver_templates.html'

    def get_context_data(self, **kwargs):
        context = super(ver_templatesTemplate, self).get_context_data(**kwargs)

        context['templates'] = Template.objects.all()
        return context


class revisarTemplate(LoginRequiredMixin,TemplateView):
    login_url = '/login/'
    redirect_field_name = '/'
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)
        prev = request.GET.get('type')

        if prev is not None:
            context['page_name'] = prev
        else:
            context['page_name'] = 'revisar'

        template = Template.objects.get(id=(kwargs['templateID']))
        patterns = template.sorted_patterns()
        print(patterns)
        context['patterns'] = template.sorted_patterns()
        context['tem_id'] = kwargs['templateID']

        return self.render_to_response(context)


class editarTemplate(LoginRequiredMixin,TemplateView):
    login_url = '/login/'
    redirect_field_name = '/'
    template_name = 'builder/build.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        template = Template.objects.get(id=(kwargs['templateID']))
        patterns = template.sorted_patterns()
        components = TemplateComponent
        for pattern in patterns:
            print(pattern.template_component.get().position)
        context['patterns'] = patterns
        context['tem_id'] = kwargs['templateID']
        context['tem_name'] = template.name
        context['captchaHTML'] = render_to_string('patrones/captcha/captcha.html', { 'public_key':'demoPublicKey' })
        #context['page_name'] = 'preview'
        return self.render_to_response(context)


@login_required(redirect_field_name='/')
@csrf_exempt
def formConfig(request):
    if request.method == 'POST':
        user = request.user
        form_json = json.loads(request.POST['form_json'])
        template_id = int(request.POST['template'])
        position = request.POST.get('position', None)

        if position != None:
            component = TemplateComponent.objects.get(template_id=template_id, position=position)
            form = component.content_object
            form.form_json = form_json
            form.save()
        else:
            template = Template.objects.get(pk=template_id)
            patterns = template.sorted_patterns()
            if len(patterns):
                position = patterns[-1].template_component.get().position + 1
            else:
                position = 0
            form = Formulario.objects.create_pattern(form_json=form_json, template=template, position=position)

        return JsonResponse({
            "html": form.render_card(),
            "position": form.template_component.get().position,
            "form_json": form_json
        })


@csrf_exempt
def accordionConfig(request):
    if request.method == 'POST':
        # Extraemos las variables del form.
        template_id = int(request.POST.get('template', None))
        position = request.POST.get('position', None)

        # print("{} - {}\n".format(template_id, position))
        # Editando patron
        if position is not None:
            template = Template.objects.get(pk=template_id)
            component = TemplateComponent.objects.filter(
                position=int(position),
                template=template
            )
            accordion = Accordion.objects.get(template_component=component)
            accordion.save()
        else:
            # Se obtiene el template ID junto con los patrones para poder
            # configurarle la posición a este patrón.
            template = Template.objects.get(pk=template_id)
            patterns = template.sorted_patterns()

            if patterns:
                position = patterns[-1].template_component.get().position
                position += 1
            else:
                position = 0

            accordion = Accordion.objects.create_pattern(
                position=position,
                template=template
            )

        return JsonResponse({
            'position': accordion.template_component.get().position,
            'html': accordion.render_card()
        })

@csrf_exempt
def minesweepConfig(request):
    if request.method == 'POST':
        # Extraemos las variables del form.
        template_id = int(request.POST.get('template', None))
        position = request.POST.get('position', None)

        # print("{} - {}\n".format(template_id, position))
        # Editando patron
        if position is not None:
            template = Template.objects.get(pk=template_id)
            component = TemplateComponent.objects.filter(
                position=int(position),
                template=template
            )
            minesweep = Minesweep.objects.get(template_component=component)
            minesweep.save()
        else:
            # Se obtiene el template ID junto con los patrones para poder
            # configurarle la posición a este patrón.
            template = Template.objects.get(pk=template_id)
            patterns = template.sorted_patterns()

            if patterns:
                position = patterns[-1].template_component.get().position
                position += 1
            else:
                position = 0

            minesweep = Minesweep.objects.create_pattern(
                position=position,
                template=template
            )

        return JsonResponse({
            'position': minesweep.template_component.get().position,
            'html': minesweep.render_card()
        })


@login_required(redirect_field_name='/')
@csrf_exempt
def captchaConfig(request):
    if request.method == 'POST':
        user = request.user

        # Extraemos las variables del form.
        template_id = int(request.POST.get('template', None))
        position = request.POST.get('position', None)
        public_key = request.POST.get('public_key', None)
        private_key = request.POST.get('private_key', None)

        print("{} - {}\n {}\n - {}".format(template_id, position, public_key, private_key))
        # Editando patron
        if position != None:
            template = Template.objects.get(pk=template_id)
            component = TemplateComponent.objects.filter(position=int(position), template=template)
            captcha = Captcha.objects.get(template_component=component)
            captcha.public_key = public_key
            captcha.private_key = private_key
            captcha.save()
        else:
            # Se obtiene el template ID junto con los patrones para poder
            # configurarle la posición a este patrón.
            template = Template.objects.get(pk=template_id)
            patterns = template.sorted_patterns()

            if patterns:
                position = patterns[-1].template_component.get().position
                position += 1
            else:
                position = 0

            captcha = Captcha.objects.create_pattern(public_key = public_key,
                                                     private_key = private_key,
                                                     position = position,
                                                     template = template)

        return JsonResponse({
            'position': captcha.template_component.get().position,
            'html': captcha.render_card()
        })

@login_required(redirect_field_name='/')
def eraseCaptcha(request):

    template_id = request.GET.get('template', None)
    position = request.GET.get('position', None)
    print(template_id,position)
    component = TemplateComponent.objects.filter(position=int(position), template_id=int(template_id))
    captcha = Captcha.objects.get(template_component=component)
    captcha.delete()
    return JsonResponse(data={})

@csrf_exempt
@login_required(redirect_field_name='/')
def navbarConfig(request):
    if request.method == 'POST':
        # Extraemos las variables del form.
        template_id = int(request.POST.get('template', None))
        position = request.POST.get('position', None)
        elementos = json.loads(request.POST.get('elementos',None))

        # Editando patron
        if position != None:
            template = Template.objects.get(pk=template_id)
            component = TemplateComponent.objects.filter(position=int(position), template=template)
            navbar = Navbar.objects.get(template_component=component)
            navbar.elementos = elementos
            navbar.save()
        else:
            # Se obtiene el template ID junto con los patrones para poder
            # configurarle la posición a este patrón.
            template = Template.objects.get(pk=template_id)
            patterns = template.sorted_patterns()

            if patterns:
                position = patterns[-1].template_component.get().position
                position += 1
            else:
                position = 0

            navbar = Navbar.objects.create_pattern(elementos = elementos,
                                                   position = position,
                                                   template = template)

        return JsonResponse({
            'position': navbar.template_component.get().position,
            'html': navbar.render_card()
        })

@csrf_exempt
@login_required(redirect_field_name='/')
def pollConfig(request):
    user = request.user
    question_text = request.POST.get('pregunta', None)
    options = request.POST.getlist('opciones[]', None)
    template_pk = request.POST.get('template', None)
    position = request.POST.get('position', None)


    if position != None:
        template = Template.objects.get(pk=int(template_pk))
        component = TemplateComponent.objects.get(position=int(position), template=template)
        question = Pregunta.objects.get(template_component=component)
        question.texto_pregunta = question_text
        Opcion.objects.filter(pregunta=question).delete()

        print(options)
        for option in options:
            Opcion.objects.create(pregunta=question, texto_opcion=option).save()

        question.save()
    else:
        template = Template.objects.get(id=int(template_pk))
        patterns = template.sorted_patterns()

        if patterns:
            position = patterns[-1].template_component.get().position
            position += 1
        else:
            position = 0

        question = Pregunta.objects.create_pattern(texto_pregunta=question_text, position=position, template=template)

        for option in options:
            Opcion.objects.create(pregunta=question, texto_opcion=option).save()

    component = question.template_component.get()

    return JsonResponse(
        data={
            'position': component.position,
            'html': question.render_card()
        }
    )

@csrf_exempt
@login_required(redirect_field_name='/')
def faqConfig(request):
    user = request.user
    category = request.POST.get('categoria', None)
    questions = request.POST.getlist('preguntas[]', None)
    answers = request.POST.getlist('respuestas[]', None)
    print(questions,answers)
    template_pk = request.POST.get('template', None)
    position = request.POST.get('position', None)


    if position is not None:
        template = Template.objects.get(pk=int(template_pk))
        component = TemplateComponent.objects.get(position=int(position), template=template)
        faq = Faq.objects.get(template_component=component)
        faq_category = faq.categoria_set.all()[0]
        faq_category.nombre = category
        faq_category.save()

        faq.preguntafaq_set.all().delete()

        for i,question in enumerate(questions):
            PreguntaFaq.objects.create(faq=faq, tema=faq_category, pregunta=question, respuesta=answers[i]).save()

        questions = PreguntaFaq.objects.filter(faq=faq).order_by('id')
        print(questions)
        return JsonResponse(
            data={
            'position': faq.template_component.get().position,
            'html': faq.render_card()
            })

    else:
        template = Template.objects.get(id=int(template_pk))
        patterns = template.sorted_patterns()

        if patterns:
            position = patterns[-1].template_component.get().position
            position += 1
        else:
            position = 0

        faq = Faq.objects.create_pattern(position=position, template=template)
        faq.save()
        print(faq)

        if category != '':
            category = Categoria.objects.create(faq=faq,nombre=category).save()
        for i,question in enumerate(questions):
            PreguntaFaq.objects.create(faq=faq, tema=category, pregunta=question, respuesta=answers[i]).save()
        questions = PreguntaFaq.objects.filter(faq=faq).order_by('id')
        print(questions)
        return JsonResponse(
            data={
            'position': faq.template_component.get().position,
            'html': faq.render_card()
            })

@login_required(redirect_field_name='/')
def newTemplate(request):
    name = request.GET.get('name', None)
    template = Template.objects.create(name=name)
    pk = template.pk
    template.save()
    return JsonResponse(data={'id': str(pk)})


@login_required(redirect_field_name='/')
def eraseQuestion(request):

    template_id = request.GET.get('template', None)
    position = request.GET.get('position', None)
    print(template_id,position)
    component = TemplateComponent.objects.filter(position=int(position), template_id=int(template_id))
    question = Pregunta.objects.get(template_component=component)
    question.delete()
    return JsonResponse(data={})

@login_required(redirect_field_name='/')
def createPoll(request):
    template_id = request.GET.get('template', None)
    template = Template.objects.get(id=int(template_id))
    patterns = template.sorted_patterns()

    if patterns:
        position = patterns.last().get().position
        position += 1
    else:
        position = 0

    return JsonResponse(data={'position':position,})

class userTemplate(TemplateView):
    template_name = 'crear_usuario.html'

    def get_context_data(self, **kwargs):
        context = super(userTemplate, self).get_context_data(**kwargs)
        context['form'] = registerForm()
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = registerForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/')

        else:
            form = registerForm()

        return render(request, 'crear_usuario.html',{'form': form})

class loginTemplate(TemplateView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super(loginTemplate, self).get_context_data(**kwargs)
        context['form'] = loginForm()
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = loginForm(request.POST)
            if form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username,password=password)

                if user is not None:
                    login(request,user)
                    return HttpResponseRedirect('/')

        else:
            form = registerForm()

        return render(request, 'login.html',{'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

@login_required(redirect_field_name='/')
def configModal(request):
    if 'pattern-name' in request.GET:
        # Si se esta agregando un nuevo patron, se crea una instancia dummy y se llama a render_config_form de esta
        # (con sus campos vacios)
        pattern_name = request.GET['pattern-name']
        # workaround porque el modelo no se llama igual que el patron
        if pattern_name == 'encuesta':
            pattern_name = 'pregunta'
        ct = ContentType.objects.get(model=pattern_name)
        pattern_class = ct.model_class()
        pattern = pattern_class()
    # Si se esta editando un patron ya existente se pasa el template_component id y se saca el patron de ahi
    elif 'template-component-id' in request.GET:
        pattern = TemplateComponent.objects.get(id=request.GET['template-component-id']).content_object
    return HttpResponse(pattern.render_config_modal(request), request)

@login_required(redirect_field_name='/')
def deletePattern(request):
    component = TemplateComponent.objects.get(pk=request.GET['template-component-id'])
    deleted = component.delete()
    return JsonResponse(data={'deleted': deleted})
