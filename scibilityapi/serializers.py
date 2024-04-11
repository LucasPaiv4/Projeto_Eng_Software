from scibilityapi.models import Projetos, Habilidades, HabilidadesProjeto
from rest_framework import serializers

        
class HabilidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habilidades
        fields = ['id', 'nome']
        
    # def create(self, validated_data):
    #     projeto_id = self.context['projeto_id']
    #     return Habilidades.objects.create(projeto_id=projeto_id, **validated_data)
        
class ProjetoSerializer(serializers.ModelSerializer):
    habilidades = HabilidadeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Projetos
        fields = ['id', 'nome', 'email', 'descricao', 'habilidades']