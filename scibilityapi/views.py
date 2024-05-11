from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet

from scibilityapi.utils import enviar_email_de_interesse
from .models import Projetos, Habilidades, HabilidadesProjeto, Usuario, HabilidadesUsuario, InteresseProjeto
from .serializers import ProjetoSerializer, HabilidadeSerializer, UsuarioSerializer, InteresseProjetoSerializer
from .permissions import IsOwnerOrReadOnly

class ProjetoViewSet(ModelViewSet):
    queryset = Projetos.objects.all()
    serializer_class = ProjetoSerializer
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def demonstrar_interesse(self, request, pk=None):
        projeto = self.get_object()
        usuario = request.user.usuario
        # Verifica se o usuário já demonstrou interesse anteriormente
        interesse_existente = InteresseProjeto.objects.filter(usuario=usuario, projeto=projeto).exists()
        if not interesse_existente:
            InteresseProjeto.objects.create(usuario=usuario, projeto=projeto)
            enviar_email_de_interesse(projeto.email, projeto.nome, usuario.user.username, usuario.user.email)
            return Response({"status": "interesse registrado"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "interesse já registrado"}, status=status.HTTP_409_CONFLICT)
        
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def remover_interesse(self, request, pk=None):
        projeto = self.get_object()
        usuario = request.user.usuario
        try:
            interesse = InteresseProjeto.objects.get(usuario=usuario, projeto=projeto)
            interesse.delete()
            return Response({"status": "interesse removido"}, status=status.HTTP_204_NO_CONTENT)
        except InteresseProjeto.DoesNotExist:
            return Response({"error": "interesse não encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        else:
            permission_classes = [IsAuthenticated]  # Padrão para quaisquer outras ações
        return [permission() for permission in permission_classes]
    
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
    #permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get', 'patch'], url_path='me', permission_classes=[IsAuthenticated])
    def get_me(self, request):
        if request.method == 'GET':
            usuario = request.user.usuario
            serializer = self.get_serializer(usuario)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(request.user.usuario, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
    
    # @action(detail=False, methods=['GET', 'PUT'])
    # def me(self, request):
    #     usuario = request.user.usuario
    #     if request.method == 'GET':
    #         serializer = UsuarioSerializer(usuario)
    #         return Response(serializer.data)
    #     elif request.method == 'PUT':
    #         serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data)
    
    # @action(detail=False, methods=['GET', 'PUT'])
    # def me(self, request):
    #     (usuario, created) = Usuario.objects.get_or_create(user_id=request.user.id)
    #     if request.method == 'GET':
    #         serializer = UsuarioSerializer(usuario)
    #         return Response(serializer.data)
    #     elif request.method == 'PUT':
    #         serializer = UsuarioSerializer(usuario, data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data)

class HabilidadeUsuarioViewSet(ModelViewSet):
    serializer_class = HabilidadeSerializer
    
    def get_queryset(self):
        usuario_id = self.request.user.usuario.id
        return Habilidades.objects.filter(habilidadesusuario__pessoa_id=usuario_id)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = request.user.usuario
        habilidade = serializer.save()
        HabilidadesUsuario.objects.create(pessoa=usuario, habilidade=habilidade)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
    
class InteresseProjetoViewSet(ModelViewSet):
    queryset = InteresseProjeto.objects.all()
    serializer_class = InteresseProjetoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user.usuario)

    def get_queryset(self):
        # Filtrar interesses para o usuário logado apenas
        if self.action == 'list':
            return self.queryset.filter(usuario=self.request.user.usuario)
        return self.queryset
