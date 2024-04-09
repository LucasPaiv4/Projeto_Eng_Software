from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
#from rest_framework import status
from .models import Projetos, Habilidades
from .serializers import ProjetoSerializer, HabilidadeSerializer

class ProjetoViewSet(ModelViewSet):
    queryset = Projetos.objects.all()
    serializer_class = ProjetoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nome']
    
class HabilidadeViewSet(ModelViewSet):
    queryset = Habilidades.objects.all()
    serializer_class = HabilidadeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nome']