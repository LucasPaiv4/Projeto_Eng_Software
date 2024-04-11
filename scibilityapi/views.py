from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import Projetos, Habilidades, HabilidadesProjeto
from .serializers import ProjetoSerializer, HabilidadeSerializer

class ProjetoViewSet(ModelViewSet):
    queryset = Projetos.objects.all()
    serializer_class = ProjetoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nome']
    
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