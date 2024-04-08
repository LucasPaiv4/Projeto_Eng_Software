from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Projetos, Habilidades
from .serializers import ProjetoSerializer, HabilidadeSerializer

@api_view(['GET', 'POST'])
def project_list(request):
    if request.method == 'GET':
        queryset = Projetos.objects.all()
        serializer = ProjetoSerializer(queryset, many=True, 
                                       context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProjetoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@api_view(['GET', 'PUT', 'DELETE'])
def project_detail(request, id):
    projeto = get_object_or_404(Projetos, pk=id)
    if request.method == 'GET':
        serializer = ProjetoSerializer(projeto)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProjetoSerializer(projeto, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        projeto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)