from django.test import TestCase
from django.test.utils import setup_test_environment
from django.urls import reverse
from ..models import KeyPair, GeneratedCaptcha

setup_test_environment()


class ValidateCaptchaTest(TestCase):
    """ Clase de pruebas para el endpoint de validación de captchas.
    """
    def setUp(self):
        """
        Función que se encarga de crear dos captchas con sus respectivos KeyPair
        junto con una respuesta errónea antes de ejecutar cada caso de prueba.
        """
        keypair = KeyPair()
        keypair.save()
        self._testing_captcha = GeneratedCaptcha(keypair=keypair,
                                                 answer="test01")
        self._testing_captcha.save()

        keypair = KeyPair()
        keypair.save()
        self._testing_captcha_2 = GeneratedCaptcha(keypair=keypair,
                                                   answer="test02")
        self._testing_captcha_2.save()
        self._wrong_answer = "wrong1"

    def test_post_method(self):
        """
        Prueba para ver que se recibe un OK cuando se utiliza el
        método POST con datos y error sin datos.
        """
        response_no_data = \
            self.client.post(path=reverse('validate_captcha'))
        response_with_data = \
            self.client.post(path=reverse('validate_captcha'),
                             data={"user_answer": self._testing_captcha.answer,
                                   "captcha_id": self._testing_captcha.captcha_id,
                                   "private_key": self._testing_captcha.keypair.private_key,
                                   })

        self.assertEqual(response_no_data.status_code, 200)
        self.assertEqual(response_with_data.status_code, 200)

    def test_get_method(self):
        """
        Prueba para ver que se recibe un NoSupported cuando se utiliza el método
        GET con o sin datos.
        """
        response_no_data = \
            self.client.get(path=reverse('validate_captcha'))
        response_with_data = \
            self.client.get(path=reverse('validate_captcha'),
                             data={"user_answer": self._testing_captcha.answer,
                                   "captcha_id": self._testing_captcha.captcha_id,
                                   "private_key": self._testing_captcha.keypair.private_key,
                                   })

        self.assertEqual(response_no_data.status_code, 405)
        self.assertEqual(response_with_data.status_code, 405)

    def test_put_method(self):
        """
        Prueba para ver que se recibe un NotSupported cuando se utiliza el
        método PUT
        """
        response_no_data = \
            self.client.put(path=reverse('validate_captcha'))
        response_with_data = \
            self.client.put(path=reverse('validate_captcha'),
                             data={"user_answer": self._testing_captcha.answer,
                                   "captcha_id": self._testing_captcha.captcha_id,
                                   "private_key": self._testing_captcha.keypair.private_key,
                                   })

        self.assertEqual(response_no_data.status_code, 405)
        self.assertEqual(response_with_data.status_code, 405)

    def test_response_correct_answer(self):
        """
        Prueba para verificar que la respuesta cuando se entregan los datos
        válidos y una respuesta inválida.
        """
        response = \
            self.client.post(path=reverse('validate_captcha'),
                            data={"user_answer": self._testing_captcha.answer,
                                  "captcha_id": self._testing_captcha.captcha_id,
                                  "private_key": self._testing_captcha.keypair.private_key,
                                  })
        data = response.json()
        self.assertEqual(data['error'], "")
        self.assertTrue(expr=data['success'])

    def test_response_wrong_answer(self):
        """
        Prueba para verificar que la respuesta cuando se entregan los datos
        válidos y una respuesta inválida.
        """
        response = \
            self.client.post(path=reverse('validate_captcha'),
                            data={"user_answer": self._wrong_answer,
                                  "captcha_id": self._testing_captcha.captcha_id,
                                  "private_key": self._testing_captcha.keypair.private_key,
                                  })
        data = response.json()
        self.assertEqual(data['error'], "")
        self.assertFalse(expr=data['success'])

    def test_response_missing_field(self):
        """
        Prueba para verificar que si un campo POST no se envía hay que devolver
        un error.
        """
        response = \
            self.client.post(path=reverse('validate_captcha'),
                            data={"user_answer": self._testing_captcha.answer,
                                  "private_key": self._testing_captcha.keypair.private_key,
                                  })
        data = response.json()
        self.assertEqual(data['error'], "Falta el campo captcha_id")

    def test_response_privatekey_nonexisting(self):
        """
        Prueba para verificar el comportamiento del API cuando se recibe una
        clave privada que no existe.
        """
        response = \
            self.client.post(path=reverse('validate_captcha'),
                            data={"user_answer": self._testing_captcha.answer,
                                  "captcha_id": self._testing_captcha.captcha_id,
                                  "private_key": self._testing_captcha.keypair.private_key.swapcase(),
                                  })
        data = response.json()
        self.assertEqual(data['error'], "Fallo de autenticacion")

    def test_response_captchaid_nonexisting(self):
        """
        Prueba para verificar el comportamiento del API cuando se recibe una
        clave privada que no existe.
        """
        response = \
            self.client.post(path=reverse('validate_captcha'),
                            data={"user_answer": self._testing_captcha.answer,
                                  "captcha_id": self._testing_captcha.captcha_id.swapcase(),
                                  "private_key": self._testing_captcha.keypair.private_key,
                                  })
        data = response.json()
        self.assertEqual(data['error'], "captcha_id invalido")

    def test_response_captchaid_keypair_notmatching(self):
        """
        Prueba para verificar si hay error cuando se manda un KeyPair válido
        pero que no fue usado para generar el captcha actual.
        """
        response_captchaid_ok_keypair_notok = \
            self.client.post(path=reverse('validate_captcha'),
                            data={"user_answer": self._testing_captcha.answer,
                                  "captcha_id": self._testing_captcha.captcha_id,
                                  "private_key": self._testing_captcha_2.keypair.private_key,
                                  })

        response_captchaid_notok_keypair_ok = \
            self.client.post(path=reverse('validate_captcha'),
                            data={"user_answer": self._testing_captcha.answer,
                                  "captcha_id": self._testing_captcha_2.captcha_id,
                                  "private_key": self._testing_captcha.keypair.private_key,
                                  })
        data_ok_notok = response_captchaid_ok_keypair_notok.json()
        data_notok_ok = response_captchaid_notok_keypair_ok.json()

        self.assertEqual(data_ok_notok['error'],
                         "private_key no permite validar captcha_id")
        self.assertEqual(data_notok_ok['error'],
                         "private_key no permite validar captcha_id")
