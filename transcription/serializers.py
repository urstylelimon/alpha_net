from rest_framework import serializers
from .models import TranscriptionSession

class TranscriptionSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscriptionSession
        fields = '__all__'