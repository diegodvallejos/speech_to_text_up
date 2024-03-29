import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from dotenv import load_dotenv, find_dotenv
import requests
import os

load_dotenv(find_dotenv())

def generate_response(audio_file):
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    headers = {"Authorization": f"Bearer {os.environ.get('WHISPER_API_KEY')}"}

    with open(audio_file, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

class WhisperASR():
    """
    This class represents a speech-to-text model using the Whisper ASR model.
    
    Attributes:
        device (str): The device to use for inference (e.g., "cuda:0" for GPU or "cpu" for CPU).
        torch_dtype (torch.dtype): The torch data type to use for model inference.
        model (AutoModelForSpeechSeq2Seq): The pre-trained Whisper ASR model.
        processor (AutoProcessor): The pre-trained processor for the Whisper ASR model.
        pipe (ASRPipeline): The pipeline for automatic speech recognition using the Whisper ASR model.
    """
   
    def __init__(self):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        model_id = "openai/whisper-whisper-large-v3"

        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=self.torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        self.model.to(self.device)

        self.processor = AutoProcessor.from_pretrained(model_id)

        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            max_new_tokens=128,
            chunk_length_s=30,
            batch_size=16,
            return_timestamps=True,
            torch_dtype=self.torch_dtype,
            device=self.device,
        )
        
    def to_text(self, input):
        """
        Transcribes the input speech to text using the Whisper ASR model.
        
        Args:
            input (str): The input speech to transcribe.
        """
        self.content = self.pipe(input)
        self.text = self.content[0]["text"]
        self.timestamps = self.content[0]["chunks"]
            
    # def text(self):
    #     """
    #     Returns the transcribed text from the most recent call to `to_text` method.
        
    #     Returns:
    #         str: The transcribed text.
    #     """
    #     return self.text[0]["text"]
        
    # def timestamps(self):
    #     """
    #     Returns the timestamps of the transcribed chunks from the most recent call to `to_text` method.
        
    #     Returns:
    #         list: A list of dictionaries containing the start and end timestamps of each transcribed chunk.
    #     """
    #     return self.text[0]["chunks"]
