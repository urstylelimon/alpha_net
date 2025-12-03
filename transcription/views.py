from django.shortcuts import render
from rest_framework import viewsets
from .models import TranscriptionSession
from .serializers import TranscriptionSessionSerializer
def index(request):
    return render(request, 'transcription/index.html')

class SessionViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = TranscriptionSession.objects.all().order_by('-start_time')
    serializer_class = TranscriptionSessionSerializer