import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset

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

        model_id = "openai/whisper-large-v3"

        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        model.to(device)

        self.processor = AutoProcessor.from_pretrained(model_id)

        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            max_new_tokens=128,
            chunk_length_s=30,
            batch_size=16,
            return_timestamps=True,
            torch_dtype=torch_dtype,
            device=device,
        )
        
    def to_text(self, input):
        """
        Transcribes the input speech to text using the Whisper ASR model.
        
        Args:
            input (str): The input speech to transcribe.
        """
        self.text = self.pipe(input)
            
    def text(self):
        """
        Returns the transcribed text from the most recent call to `to_text` method.
        
        Returns:
            str: The transcribed text.
        """
        return self.text[0]["text"]
        
    def timestamps(self):
        """
        Returns the timestamps of the transcribed chunks from the most recent call to `to_text` method.
        
        Returns:
            list: A list of dictionaries containing the start and end timestamps of each transcribed chunk.
        """
        return self.text[0]["chunks"]


# example usage
# asr = WhisperASR()

# dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")
# sample = dataset[0]["audio"]

# asr.to_text(sample)
# print(asr.timestamps())