# Documentación sobre los endpoints provistos.
En el presente documento se detallará las características y operaciones realizadas por cada endpoint provisto para el manejo de los captchas.

## Generación de un APIKEY.
- Acceso: método GET.
- URL: /servecaptcha/generate_apikey/

- Entrada: Ninguna

- Acciones:
	- Crea un APIKEY para el diseñador.

- Retorna: las claves publica y privadas para el diseñador
- Ejemplo:
```json
{
	"private_key": "2fPJffRPuN7p5KXkH31INq3rjJUUkv7k0OmxTFJJjABNij02tnKFPUaxQYrK1tSv",
	"public_key": "7knp9uBfCZH7W4JZ5OR4xCgU2CNxgQvLDf20i5hPnrNFj39dFpsAnxQm7JeB4PPZ"
}
```

## Generación de un CAPTCHA.
- Acceso: método GET.
- URL: /servecaptcha/generate_captcha/public_key/

- Entrada:
	- Llave pública del diseñador en public_key

- Acciones:
	- Buscar el APIKEY asociado a la llave pública.
	- Generar aleatoriamente una respuesta.
	- Generar un CAPTCHA asociando la respuesta con el APIKEY.

- Retorna:
	- Error, vacio si no hay problemas, con un mensaje si public_key es invalido
	- ID del captcha creado (captcha_id).
- Ejemplo de respuesta sin error:
```json
{
	"error": "",
	"captcha_id": "75xuqo9jckekZphLibJFrmKCENVbwEvY31LymjJ97jz3PGPjzJr9M5NBhTt6arXs"
}
```
- Ejemplo de respuesta con error:
```json
{"error": "APIKEY inexistente"}
```

## Validación de un CAPTCHA.
- Acceso: método POST.
- URL: /servecaptcha/validate_captcha/

- Entrada:
	- Respuesta del usuario (user_answer).
	- CAPTCHAID (captcha_id).
	- LLave privada asociada al CAPTCHA (private_key).

- Acciones:
	- Verificar que el formulario sea válido.
	- Buscar el CAPTCHA dentro de la BD con el CAPTCHAID.
	- Buscar el APIKEY asociado el CAPTCHA dentro de la BD con la llave privada.
	- Verificar que la respuesta del usuario sea la que corresponde en el CAPTCHA.
	- Verificar que el APIKEY buscado en la BD sea el mismo al asociado al CAPTCHA.

- Retorna: Es válido o no el CAPTCHA con la información pasada. Un mensaje
	de error si algun parametro es invalido.
- Ejemplo de llamada:

```bash
curl --data \ "captcha_id=wH3ljVPRbqt38Y08ZdIAjQk5RrYzDBfAl4yDVDvrAOh3SGKpPxqxNbKxfYuOtIUF3Pd9eX81Ex1p9eHJ14bTTg0&user_answer=270497" \
localhost:8000/servecaptcha/validate_captcha/
```
- Respuesta si user_answer es correcto:
```json
{"error": "", "success": true}
```
- Respuesta si user_answer es incorrecto:
```json
{"error": "", "success": false}
```
- Respuesta si falta un parametro (captcha_id en este caso):
```json
{"error": "Falta el campo captcha_id"}
```
- Respuesta con private_key inexistente:
```json
{"error": "Fallo de autenticacion"}
```
- Respuesta con captcha_id inexistente:
```json
{"error": "captcha_id invalido"}
```
- Respuesta si el usuario no tiene permitido validar el captcha:
```json
{"error": "private_key no permite validar captcha_id"}
```
