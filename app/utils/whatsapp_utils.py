import logging
from flask import current_app, jsonify
import json
import requests

from app.services.whisper_service import generate_response
import re
import os
import time


def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")


def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )
    

def get_audio_file_url(audio_id):
    url = f"https://graph.facebook.com/v19.0/{audio_id}/"
    headers = {
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(data)
        audio_url = data["url"]
        print(audio_url)
        return audio_url
    except requests.RequestException as e:
        logging.error(f"Failed to get audio file URL: {e}")
        return None
    

def download_audio_file(audio_id):
    url = get_audio_file_url(audio_id)
    headers = {
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        with open(f"audios/{audio_id}.ogg", "wb") as file:
            file.write(response.content)
        return True
    except requests.RequestException as e:
        logging.error(f"Failed to download audio file: {e}")
        return False
    

def upload_audio_file(media_id):
    url = f"https://graph.facebook.com/v19.0/{media_id}/media"
    headers = {
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}"
    }
    files = {
        "file": open("audios/prueba.ogg", "rb")
    }
    data = {
        "type": "audio/ogg",
        "messaging_product": "whatsapp"
    }

    try:
        response = requests.post(url, headers=headers, files=files, data=data)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logging.error(f"Failed to upload audio file: {e}")
        return False
    
        
def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    try:
        response = requests.post(
            url, data=data, headers=headers, timeout=10
        )  # 10 seconds timeout as an example
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except (
        requests.RequestException
    ) as e:  # This will catch any general request exception
        logging.error(f"Request failed due to: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        # Process the response as normal
        log_http_response(response)
        return response


def process_text_for_whatsapp(text):
    # Remove brackets
    pattern = r"\【.*?\】"
    # Substitute the pattern with an empty string
    text = re.sub(pattern, "", text).strip()

    # Pattern to find double asterisks including the word(s) in between
    pattern = r"\*\*(.*?)\*\*"

    # Replacement pattern with single asterisks
    replacement = r"*\1*"

    # Substitute occurrences of the pattern with the replacement
    whatsapp_style_text = re.sub(pattern, replacement, text)

    return whatsapp_style_text


def process_whatsapp_message(body):
    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]

    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    
    if message["type"] == "text":
        send_message(get_text_message_input(current_app.config["RECIPIENT_WAID"], "Por favor, envíame un audio."))
        raise Exception("Invalid message type. Expected audio, received text.")
    
    audio_id = message["audio"]["id"]
    
    download_audio_file(audio_id)
    
    audio_file = f"audios/{audio_id}.ogg"
    
    response = generate_response(audio_file)

    data = get_text_message_input(current_app.config["RECIPIENT_WAID"], response["text"])
    send_message(data)

    """ TODO: 
        - crear logica para cuando nos envian un texto en vez de un audio
    """


def is_valid_whatsapp_message(body):
    """
    Check if the incoming webhook event has a valid WhatsApp message structure.
    """
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )
