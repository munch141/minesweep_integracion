from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import escape
from django.http import HttpResponse, HttpResponseNotAllowed, Http404, JsonResponse


def index(request):
    captchaHTML = render_to_string('tuisd/captcha/captcha.html', { 'public_key':'demoPublicKey' })
    return render(request, 'formBuilder/index.html', { 'escapedCaptchaHTML': escape(captchaHTML) })
