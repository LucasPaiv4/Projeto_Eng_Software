from scibilityapi.models import Project, Hability
from rest_framework import serializers

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'nome', 'email', 'descricao']
        
class HabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hability
        fields = ['id', 'nome']