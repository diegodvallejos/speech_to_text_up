## WhatsApp Bot Speech-to-Text with OpenAI Whisper

Este repositorio permite implementar un bot en WhatsApp que convierte mensajes de voz enviados por los usuarios en texto utilizando el modelo de lenguaje de OpenAI Whisper, específicamente el modelo whisper-large-v3.

## Cómo Funciona

El bot en WhatsApp se configura utilizando Meta for Developers para interactuar con la API de WhatsApp. Esto se logra mediante un webhook que permite que un número de teléfono actúe como un bot. Cada vez que un usuario envía un mensaje, este se recibe y procesa utilizando Python.

### Proceso de Conversión

1. Cuando un usuario envía un mensaje de voz a través de WhatsApp, el bot recibe la solicitud a través del webhook.

2. El mensaje de voz se procesa utilizando el modelo de lenguaje de OpenAI Whisper, que se encuentra en la versión whisper-large-v3.

3. Una vez que se completa la inferencia, el mensaje de voz se convierte en texto.

4. El texto resultante se envía de vuelta al usuario como respuesta al mensaje original de voz.

## Requisitos

- Python 3.10.4
- Cuenta en ngrok para obtener un dominio gratuito en desarrollo.

## Configuración

Para ejecutar la aplicación, sigue estos pasos:

1. Instala las dependencias requeridas ejecutando el siguiente comando:

```bash
pip install -r requirements.txt
```

2. Configura una cuenta en ngrok para obtener un dominio gratuito en desarrollo. Este dominio será necesario para probar el bot desde WhatsApp y también se utilizará al crear el webhook.

3. Crea una cuenta de Meta for Developers y ahi dentro deberás crar una nueva app. Una vez creada deberás añadir whatsapp a tu nueva aplicación y configurar un webhook. Para más información, visitá la documentación de [cloud API]([https://github.com/](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started)) de Meta.

4. Ejecuta la aplicación Flask para abrir una conexión con el dominio asociado a la aplicación:

```bash
python run.py
```

5. Desde otra terminal, ejecuta ngrok http 8000 --domain [nombre del dominio de ngrok] para establecer el "túnel" que permite que WhatsApp acceda a la aplicación.

## Contribución

Si deseas contribuir a este proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama (`git checkout -b feature/nueva-caracteristica`).
3. Haz tus cambios y realiza un commit (`git commit -am 'Añade nueva característica'`).
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`).
5. Crea un nuevo Pull Request.

## Licencia

Este proyecto está bajo la Licencia Apache-2.0. Consulta el archivo `LICENSE` para obtener más detalles.

---

¡Esperamos que disfrutes utilizando nuestra aplicación para convertir mensajes de voz de WhatsApp en texto! Si tienes alguna pregunta o sugerencia, no dudes en ponerte en contacto con nosotros.
