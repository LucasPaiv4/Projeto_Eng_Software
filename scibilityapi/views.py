from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from .models import Projetos, Habilidades, HabilidadesProjeto, Usuario
from .serializers import ProjetoSerializer, HabilidadeSerializer, UsuarioSerializer

class ProjetoViewSet(ModelViewSet):
    queryset = Projetos.objects.all()
    serializer_class = ProjetoSerializer
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
    
class HabilidadeViewSet(ModelViewSet):
    serializer_class = HabilidadeSerializer
    
    def get_queryset(self):
        projeto_id = self.kwargs['projeto_pk']
        return Habilidades.objects.filter(habilidadesprojeto__projeto=projeto_id)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        projeto_id = self.kwargs['projeto_pk']
        projeto = Projetos.objects.get(id=projeto_id)
        habilidade = serializer.save()
        HabilidadesProjeto.objects.create(projeto=projeto, habilidade=habilidade)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_serializer_context(self):
        return {'projeto_id': self.kwargs['projeto_pk']}
    
class UsuarioViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        (usuario, created) = Usuario.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = UsuarioSerializer(usuario, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
            