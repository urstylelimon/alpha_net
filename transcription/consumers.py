import json
import vosk
import os
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime
from .models import TranscriptionSession

MODEL_PATH = "model/vosk-model-small-en-us-0.15"

if os.path.exists(MODEL_PATH):
    print("Vosk Model Found.")
    vosk_model = vosk.Model(MODEL_PATH)
    print("Model Loaded.")
else:
    print(f"Model not found at {MODEL_PATH}")
    vosk_model = None


class TranscriptionConsumer(WebsocketConsumer):
    def connect(self):
        print("Client is trying to connect...")
        if not vosk_model:
            print("Closing connection because Model is missing.")
            self.close()
            return

        self.accept()
        print("Connection Accepted!")

        self.recognizer = vosk.KaldiRecognizer(vosk_model, 16000)
        self.session = TranscriptionSession.objects.create()
        self.start_timestamp = datetime.now()

    def disconnect(self, close_code):
        print("Client Disconnected.")
        end_time = datetime.now()
        duration = (end_time - self.start_timestamp).total_seconds()

        final_json = json.loads(self.recognizer.FinalResult())
        final_text = final_json.get('text', '')

        print(f"Saving Session. Duration: {duration}s. Final text: {final_text}")

        self.session.end_time = end_time
        self.session.duration_seconds = duration
        self.session.final_transcript += " " + final_text
        self.session.save()

    def receive(self, text_data=None, bytes_data=None):
        if bytes_data:

            if self.recognizer.AcceptWaveform(bytes_data):
                result = json.loads(self.recognizer.Result())
                text = result.get('text', '')
                if text:
                    print(f"Final Sentence Found -> '{text}'")
                    self.session.final_transcript += " " + text
                    self.session.save()
                    self.send(text_data=json.dumps({'type': 'final', 'text': text}))
            else:
                partial = json.loads(self.recognizer.PartialResult())
                partial_text = partial['partial']
                if partial_text:
                    print(f"Partial -> '{partial_text}'")
                    self.send(text_data=json.dumps({'type': 'partial', 'text': partial_text}))