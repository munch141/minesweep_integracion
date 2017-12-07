from django.test import TestCase
from django.test.utils import setup_test_environment
from django.urls import reverse

setup_test_environment()


class GenerateApiKeyTest(TestCase):
    """ Clase de pruebas para el endpoint de generación de APIKEYs.
    """
    def test_get_method(self):
        """
        Prueba para ver que se recibe un OK cuando se utiliza el método GET
        """
        response = self.client.get(reverse('generate_apikey'))
        self.assertEqual(response.status_code, 200)

    def test_post_method(self):
        """
        Prueba para ver que se recibe un NotSupported cuando se utiliza el
        método POST con y sin datos.
        """
        response_no_data = \
            self.client.post(path=reverse('generate_apikey'))
        response_with_data = \
            self.client.post(path=reverse('generate_apikey'),
                             data={"test_str": "data", "test_num": 1})

        self.assertEqual(response_no_data.status_code, 405)
        self.assertEqual(response_with_data.status_code, 405)

    def test_put_method(self):
        """
        Prueba para ver que se recibe un NotSupported cuando se utiliza el
        método PUT
        """
        response_no_data = \
            self.client.put(path=reverse('generate_apikey'))
        response_with_data = \
            self.client.put(path=reverse('generate_apikey'),
                             data={"test_str": "data", "test_num": 1})

        self.assertEqual(response_no_data.status_code, 405)
        self.assertEqual(response_with_data.status_code, 405)

    def test_apikey_length(self):
        """
        Prueba para verificar que las llaves recibidas tengan longitud de
        64 caracteres.
        """
        response = self.client.get(reverse('generate_apikey'))
        data = response.json()
        self.assertEqual(len(data['public_key']), 64)
        self.assertEqual(len(data['private_key']), 64)

    def test_apikey_chartypes(self):
        """
        Prueba para verificar que las llaves solo incluyan letras minúsculas,
        letras mayúsculas y dígitos.
        """
        regex = r'[a-zA-Z0-9]{64}'
        response = self.client.get(reverse('generate_apikey'))
        data = response.json()
        self.assertRegex(text=data['public_key'], expected_regex=regex)
        self.assertRegex(text=data['private_key'], expected_regex=regex)

    def test_apikey_unicity(self):
        """
        Prueba para verificar que las llaves sean únicas para 10 mil llamadas.

        La probabilidad de generar una llave x, suponiendo que
        cada caracter es independiente de otro y que se distribuyen de manera
        uniforme es: (1/62)^64. El intérprete de Python arroja que esta
        probabilidad es aproximada a 1.9361182207546088e-115
        """
        numero_iteraciones = 10000
        public_set = set()
        private_set = set()
        for i in range(numero_iteraciones):
            response = self.client.get(reverse('generate_apikey'))
            data = response.json()
            self.assertNotIn(member=data['public_key'], container=public_set)
            self.assertNotIn(member=data['private_key'], container=private_set)
            public_set.add(data['public_key'])
            private_set.add(data['private_key'])
