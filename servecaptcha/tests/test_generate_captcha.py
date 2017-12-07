from django.test import TestCase
from django.test.utils import setup_test_environment
from django.urls import reverse
from ..models import KeyPair

setup_test_environment()


class GeneratedCaptchaTest(TestCase):
    """ Clase de pruebas para el endpoint de generación de captchas.
    """
    def setUp(self):
        """
        Función que se encarga de generar un keypair válido para cada caso de
        prueba.
        """
        self._testing_apikey = KeyPair()
        self._testing_apikey.save()

    def test_get_method(self):
        """
        Prueba para ver que se recibe un OK cuando se utiliza el método GET
        """
        response = self.client.get(reverse('generate_captcha',
                                           kwargs={'public_key': self._testing_apikey.public_key}))
        self.assertEqual(response.status_code, 200)

    def test_post_method(self):
        """
        Prueba para ver que se recibe un NotSupported cuando se utiliza el
        método POST con y sin datos.
        """
        response_no_data = \
            self.client.post(path=reverse('generate_captcha',
                                          kwargs={'public_key': self._testing_apikey.public_key}))
        response_with_data = \
            self.client.post(path=reverse('generate_captcha',
                                          kwargs={'public_key': self._testing_apikey.public_key}),
                             data={"test_key": self._testing_apikey})

        self.assertEqual(response_no_data.status_code, 405)
        self.assertEqual(response_with_data.status_code, 405)

    def test_put_method(self):
        """
        Prueba para ver que se recibe un NotSupported cuando se utiliza el
        método PUT
        """
        response_no_data = \
            self.client.put(path=reverse('generate_captcha',
                                          kwargs={'public_key': self._testing_apikey.public_key}))
        response_with_data = \
            self.client.put(path=reverse('generate_captcha',
                                          kwargs={'public_key': self._testing_apikey.public_key}),
                             data={"test_key": self._testing_apikey})

        self.assertEqual(response_no_data.status_code, 405)
        self.assertEqual(response_with_data.status_code, 405)

    def test_response_correct_publickey(self):
        """
        Prueba para verificar que la respuesta cuando se entrega un ID válido
        sea que el error esté vacío y el captcha_id concuerde con un regex.
        """
        response = self.client.get(reverse('generate_captcha',
                                           kwargs={'public_key': self._testing_apikey.public_key}))
        data = response.json()
        captcha_id_regex = r'[a-zA-Z0-9]{64}'
        self.assertEqual(data['error'], "")
        self.assertRegex(text=data['captcha_id'],
                         expected_regex=captcha_id_regex)

    def test_response_bad_publickey(self):
        """
        Prueba para verificar que la respuesta cuando se entrega un ID invlálido
        sea que el error no esté vacío y el campo de captcha_id no esté.
        """
        wrong_key = self._testing_apikey.public_key.swapcase()
        response = self.client.get(reverse('generate_captcha',
                                           kwargs={'public_key': wrong_key }))
        data = response.json()
        self.assertEqual(data['error'], "APIKEY inexistente")

    def test_captchaid_length(self):
        """
        Prueba para verificar que el captcha_id recibido tenga longitud de
        64 caracteres.
        """
        response = self.client.get(reverse('generate_captcha',
                                           kwargs={'public_key': self._testing_apikey.public_key}))
        data = response.json()
        self.assertEqual(data['error'], "")
        self.assertEqual(len(data['captcha_id']), 64)

    def test_captchaid_unicity(self):
        """
        Prueba para verificar que el captcha_id sea único para 10 mil llamadas.

        La probabilidad de colición de una llave, suponiendo que
        cada caracter es independiente de otro y que se distribuyen de manera
        uniforme es: (1/62)^64. El intérprete de Python arroja que esta
        probabilidad es aproximada a 1.9361182207546088e-115
        """
        numero_iteraciones = 10000
        captcha_id_set = set()
        for i in range(numero_iteraciones):
            response = self.client.get(reverse('generate_captcha',
                                               kwargs={'public_key': self._testing_apikey.public_key}))
            data = response.json()
            self.assertNotIn(member=data['captcha_id'], container=captcha_id_set)
            captcha_id_set.add(data['captcha_id'])
