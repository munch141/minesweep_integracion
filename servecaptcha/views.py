from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import escape
from django.http import HttpResponse, HttpResponseNotAllowed, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .audio_captcha import CaptchaAuditivo
from captcha.image import ImageCaptcha
from .models import KeyPair, GeneratedCaptcha
from .utils import random_string
import random
import tempfile
import markdown2

def serve_captcha_image(request, captcha_id):
    try:
        captcha = GeneratedCaptcha.objects.get(captcha_id=captcha_id)
    except GeneratedCaptcha.DoesNotExist:
        raise Http404("Captcha no existe")
    image = ImageCaptcha().generate(captcha.answer, format='png')
    response = HttpResponse(image.read(), content_type='image/png')
    return response


def serve_captcha_audio(request, captcha_id):
    try:
        captcha = GeneratedCaptcha.objects.get(captcha_id=captcha_id)
    except GeneratedCaptcha.DoesNotExist:
        raise Http404("Captcha no existe")
    with tempfile.TemporaryFile() as temp:
        temp.write(CaptchaAuditivo('servecaptcha/audio-alphabet').generate(captcha.answer.upper()))
        temp.seek(0)
        response = HttpResponse(temp.read(), content_type='audio/wav')
    return response


def api_documentation(request):
    with open('servecaptcha/docs/endpoints.md') as f:
        docs_md = f.read()
    docs_html = markdown2.markdown(docs_md, extras=['fenced-code-blocks'])
    return HttpResponse(docs_html)

@csrf_exempt
def generate_apikey(request):
    """ Función del endpoint para la generación de una APIKEY a través del método GET.

        Argumentos:
            request: Django request.

        Retorna:
            Un HTTP response OK con la llave pública del APIKEY. Error si algún
            campo no es correcto.
    """
    if request.method == 'GET':
        apikey = KeyPair()
        apikey.save()
        data = {
            'public_key': apikey.public_key,
            'private_key': apikey.private_key
        }
        response = JsonResponse(data)
    else:
        # Especificamos los métodos que acepta el endpoint.
        response = HttpResponseNotAllowed(content="Sólo se permite el método GET.", permitted_methods=["GET"])
    return response

@csrf_exempt
def generate_captcha(request, public_key: str):
    """ Función del endpoint para la generación del CAPTCHA.

        Se recibe a través del URL la llave pública del CAPTCHA que se quiere generar.
        Esta llave se busca y si es encontrada genera un CAPTCHA aleatorio asociando
        el APIKEY a éste.

        Argumentos:
            request: Django request.
            public_key: string representando la llave pública del diseñador que incluyó
                        el CAPTCHA.

        Retorna:
            Un HTTP response OK con la respuesta correcta del CAPTCHA, error si algún
            campo no es correcto.
    """
    if request.method == 'GET':
        # Como las llaves públicas son únicas, podemos utilizar el método get para
        # obtener de la BD la única instancia que debe haber, sin embargo,
        # este método puede lanzar una excepción si no se encuentra la llave pública.
        try:
            keypair = KeyPair.objects.get(public_key=public_key)
        except KeyPair.DoesNotExist:
            # return HttpResponseNotAllowed(content=["POST"])
            response = JsonResponse({'error': "APIKEY inexistente"})
        else:
            longitud_captcha = 6
            respuesta_captcha = random_string.alphanumeric(longitud_captcha)

            captcha = GeneratedCaptcha(keypair=keypair, answer=respuesta_captcha)
            captcha.save()

            data = {
                "captcha_id": captcha.captcha_id,
                "error": ""
            }
            response = JsonResponse(data)
    else:
        # Especificamos los métodos que acepta el endpoint.
        response = HttpResponseNotAllowed(content="Sólo se permite el método GET.", permitted_methods=["GET"])

    return response


@csrf_exempt
def validate_captcha(request):
    """ Funcíón del endpoint para la validación del CAPTCHA.

        Se recibe por el método POST la llave pública del CAPTCHA, el CAPTCHAID y
        la respuesta ingresada por el usuario. Seguidamente se verifica que el
        formulario sea válido según como se define en el documento de endpoints.

        Argumentos:
            request: Django request.
            captcha_id: string que representa el CAPTCHAID.
            private_key: string que representa la llave pública del diseñador que
                        incluyó el captcha.
            user_answer: string que representa la respuesta del usuario al responder
                         el captcha.

        Retorna:
            JSON con dos campos:
            error: vacio si la llamada fue exitosa, mensaje de error
                   en caso contrario.
            success: true o false dependiendo si la respuesta es correcta o no

    """
    if request.method == 'POST':
        data = {'error': ''}
        post = request.POST

        # validando que esten los campos y son validos
        for campo in ['captcha_id', 'private_key', 'user_answer']:
            if campo not in post:
                data['error'] = 'Falta el campo %s' % campo
                return JsonResponse(data)
        try:
            keypair = KeyPair.objects.get(private_key=post['private_key'])
        except KeyPair.DoesNotExist:
            data['error'] = 'Fallo de autenticacion'
            return JsonResponse(data)
        try:
            captcha = GeneratedCaptcha.objects.get(captcha_id=post['captcha_id'])
        except GeneratedCaptcha.DoesNotExist:
            data['error'] = 'captcha_id invalido'
            return JsonResponse(data)

        if keypair != captcha.keypair:
            data['error'] = 'private_key no permite validar captcha_id'
        else:
            data['success'] = post['user_answer'].lower() == captcha.answer.lower()
            captcha.delete()
        response = JsonResponse(data)
    else:
        response = HttpResponseNotAllowed(content="Sólo se permite el método POST.", permitted_methods=["POST"])
    return response

def captcha_js(request):
    js = render_to_string('tuisd/captcha/captcha.js', { 'public_key': request.GET['public_key'] })
    return HttpResponse(js)
