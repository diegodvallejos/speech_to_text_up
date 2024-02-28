# WhatsApp Speech-to-Text using OpenAI Whisper

Este proyecto es una aplicación que permite convertir mensajes de voz de WhatsApp en texto utilizando el modelo de lenguaje de OpenAI llamado Whisper. Con esta aplicación, los usuarios podrán transcribir fácilmente los mensajes de voz recibidos en WhatsApp a texto, lo que facilita la comprensión y la accesibilidad de los mensajes de audio.

## Características

- Conversión de mensajes de voz de WhatsApp a texto.
- Utiliza el modelo de lenguaje de OpenAI Whisper para transcribir los mensajes de voz con precisión.
- Interfaz fácil de usar para los usuarios de WhatsApp.

## Requisitos

- Python 3.10.4
- Instalaciones necesarias que se especifican en el archivo `requirements.txt`.

## Instalación

1. Clona este repositorio en tu máquina local utilizando el siguiente comando:

```bash
git clone https://github.com/diegodvallejos/speech_to_text_up.git
```

2. Instala las dependencias requeridas ejecutando el siguiente comando:

```bash
pip install -r requirements.txt
```

## Uso

1. Ejecuta el archivo principal de la aplicación:

```bash
python main.py
```

2. La aplicación solicitará acceso al directorio donde están almacenados los mensajes de voz de WhatsApp. Proporciona la ruta correspondiente cuando se solicite.

3. La aplicación procesará automáticamente los archivos de audio de WhatsApp y generará archivos de texto correspondientes en el mismo directorio.

4. ¡Disfruta de tus mensajes de voz de WhatsApp convertidos en texto!

## Contribución

Si deseas contribuir a este proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama (`git checkout -b feature/nueva-caracteristica`).
3. Haz tus cambios y realiza un commit (`git commit -am 'Añade nueva característica'`).
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`).
5. Crea un nuevo Pull Request.

## Créditos

Este proyecto utiliza el modelo de lenguaje de OpenAI Whisper para la conversión de voz a texto.

## Licencia

Este proyecto está bajo la Licencia Apache-2.0. Consulta el archivo `LICENSE` para obtener más detalles.

---

¡Esperamos que disfrutes utilizando nuestra aplicación para convertir mensajes de voz de WhatsApp en texto! Si tienes alguna pregunta o sugerencia, no dudes en ponerte en contacto con nosotros.