from scibilityapi.models import Projetos, Habilidades
from rest_framework import serializers

class ProjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projetos
        fields = ['id', 'nome', 'email', 'descricao']
        
class HabilidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habilidades
        fields = ['id', 'nome']