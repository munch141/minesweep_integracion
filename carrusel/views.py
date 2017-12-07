import json

from django.forms import inlineformset_factory, model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from builder.models import Template, TemplateComponent

from .forms import CarouselForm
from .models import Carousel, Content


def CarouselConfig(request):
    carousel = Carousel()

    ContentInlineFormSet = inlineformset_factory(
        Carousel, Content, fields=('title', 'description', 'image'), extra=2)

    if request.method == "POST":
        template_id = request.POST.get("template", None)
        position = request.POST.get("position", None)
        isNew = False

        if position is None:
            template = Template.objects.get(pk=int(template_id))
            patterns = template.sorted_patterns()

            if patterns:
                position = patterns[-1].template_component.get().position
                position += 1
            else:
                position = 0

            isNew = True
        else:
            template = Template.objects.get(pk=int(template_id))
            component = TemplateComponent.objects.get(position=int(position), template=template)
            carousel = Carousel.objects.get(template_component=component)

        form = CarouselForm(request.POST, request.FILES, instance=carousel)
        if form.is_valid():
            created_carousel = form.save(commit=False)
            formset = ContentInlineFormSet(
                request.POST, request.FILES, instance=created_carousel)
            if formset.is_valid():
                created_carousel.save()
                if isNew:
                    TemplateComponent.objects.create(
                        content_object=created_carousel, 
                        template_id=int(template_id), 
                        position=position
                    )
                formset.save()
                return JsonResponse({
                    'position': carousel.template_component.get().position,
                    'html': carousel.render_card()
                })
    else:
        template_id = request.GET.get("template", None)
        position = request.GET.get("position", None)

        if position is None:
            template = Template.objects.get(pk=int(template_id))
            patterns = template.sorted_patterns()

            if patterns:
                position = patterns[-1].template_component.get().position
                position += 1
            else:
                position = 0

        form = CarouselForm(instance=carousel)
        formset = ContentInlineFormSet(instance=carousel)
    return render(request, 'carrusel/configurar-modal.html', {'formset': formset, 'form': form, 'carousel': carousel})
