from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import escape
from django.http import HttpResponse
from zipfile import ZipFile
import io
import json
import tempfile
import requests

def index(request):
    return render(request, 'captcha_pattern/index.html')

def showCaptcha(request):
    return render(request, 'captcha_pattern/showCaptcha.html')

def showCaptchaCode(request):
    keypair = requests.get('http://127.0.0.1:8000/servecaptcha/generate_apikey').json()
    html = render_to_string('captcha_pattern/captcha/captcha.html', { 'public_key': keypair['public_key'] })
    js = render_to_string('captcha_pattern/captcha/captcha.js', { 'public_key': keypair['public_key'] })
    with open('captcha_pattern/static/captcha_pattern/captcha/css/style.css') as f:
        css = f.read()

    context = {
        'public_key': keypair['public_key'],
        'private_key': keypair['private_key'],
        'html': escape(html),
        'js': escape(js),
        'css': escape(css),
    }
    return render(request, 'captcha_pattern/generatedCode.html', context)

def generate_captcha_code_as_zip(request, public_key: str):
    html = render_to_string('captcha_pattern/captcha/captcha_with_includes.html', { 'public_key': public_key })

    # Copio el contenido del zip base (con los recursos estaticos, CSS, JS) para
    # no modificar el archivo. ZipFile#writestr tiene side-effects
    with open('captcha_pattern/static/captcha_pattern/captcha/zip/captcha_base.zip', 'rb') as f:
        captcha_zip = io.BytesIO(f.read())

    with ZipFile(captcha_zip, 'a') as zipfile:
        zipfile.writestr('index.html', html)

    response = HttpResponse(captcha_zip.getbuffer(), content_type='application/x-zip-compressed')
    response['Content-disposition'] = 'attachment; filename="captcha.zip"'
    return response


def demoCaptcha(request):
    "Manejo del formulario del demo"
    template_vars = {'post': False, 'success': False}
    if request.method == 'POST':
        template_vars['post'] = True
        params = request.POST
        if 'captcha_id' in params and 'user_answer' in params:
            url = 'http://127.0.0.1:8000/servecaptcha/validate_captcha/'
            validation_data = {
                'captcha_id': params['captcha_id'],
                'user_answer': params['user_answer'],
                'private_key': 'demoPrivateKey'
            }
            validation = requests.post(url, data=validation_data).json()
            if 'success' in validation and validation['success']:
                template_vars['success'] = True
    return render(request, 'captcha_pattern/captcha/demo.html', template_vars)
