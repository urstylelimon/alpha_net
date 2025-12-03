from django.db import models

class TranscriptionSession(models.Model):

    start_time = models.DateTimeField(auto_now_add=True)

    end_time = models.DateTimeField(null=True, blank=True)

    duration_seconds = models.FloatField(default=0.0)

    final_transcript = models.TextField(blank=True)