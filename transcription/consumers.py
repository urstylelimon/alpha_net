import json
import vosk
import os
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime
from .models import TranscriptionSession

MODEL_PATH = "model/vosk-model-small-en-us-0.15"

if os.path.exists(MODEL_PATH):
    vosk_model = vosk.Model(MODEL_PATH)
else:
    print(f"CRITICAL: Model not found at {MODEL_PATH}")
    vosk_model = None


class TranscriptionConsumer(WebsocketConsumer):
    def connect(self):
        if not vosk_model:
            self.close()
            return

        self.accept()
        self.recognizer = vosk.KaldiRecognizer(vosk_model, 16000)

        self.session = TranscriptionSession.objects.create()
        self.start_timestamp = datetime.now()

    def disconnect(self, close_code):

        end_time = datetime.now()
        duration = (end_time - self.start_timestamp).total_seconds()

        final_json = json.loads(self.recognizer.FinalResult())
        final_text = final_json.get('text', '')

        full_transcript = self.session.final_transcript + " " + final_text

        count = len(full_transcript.strip().split()) if full_transcript.strip() else 0

        self.session.final_transcript = full_transcript
        self.session.end_time = end_time
        self.session.duration_seconds = duration
        self.session.word_count = count
        self.session.save()

    def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            if self.recognizer.AcceptWaveform(bytes_data):
                result = json.loads(self.recognizer.Result())
                text = result.get('text', '')
                if text:
                    self.session.final_transcript += " " + text
                    self.session.save()
                    self.send(text_data=json.dumps({'type': 'final', 'text': text}))
            else:
                partial = json.loads(self.recognizer.PartialResult())
                partial_text = partial.get('partial', '')
                if partial_text:
                    self.send(text_data=json.dumps({'type': 'partial', 'text': partial_text}))