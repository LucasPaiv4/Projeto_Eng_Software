from scibilityapi.models import HabilidadesUsuario, Projetos, Habilidades, HabilidadesProjeto, Usuario
from rest_framework import serializers

        
class HabilidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habilidades
        fields = ['id', 'nome']
        
    # def create(self, validated_data):
    #     projeto_id = self.context['projeto_id']
    #     return Habilidades.objects.create(projeto_id=projeto_id, **validated_data)

class ProjetoSimplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projetos
        fields = ['id', 'nome']
 
class UsuarioSimplesSerializer(serializers.ModelSerializer):
    nome_completo = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Usuario
        fields = ['id', 'nome_completo']
        
    def get_nome_completo(self, obj):
        return f'{obj.first_name} {obj.last_name}'
                        
class UsuarioSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    nome_completo = serializers.SerializerMethodField(read_only=True)
    habilidades = HabilidadeSerializer(many=True, read_only=True)
    projetos = ProjetoSimplesSerializer(many=True, read_only=True, source='user.projeto_usuario')
    
    class Meta:
        model = Usuario
        fields = ['id', 'user_id', 'nome_completo', 'descricao', 'projetos', 'habilidades']
        
    def get_nome_completo(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'
        
# class HabilidadeUsuarioSerializer(serializers.ModelSerializer):
#     usuario = UsuarioSerializer()
#     habilidades = HabilidadeSerializer(many=True)
    
#     class Meta:
#         model = HabilidadesUsuario  
#         fields = ['usuario', 'habilidades']
        
class ProjetoSerializer(serializers.ModelSerializer):
    habilidades = HabilidadeSerializer(many=True, read_only=True)
    usuario = UsuarioSimplesSerializer(read_only=True)
    
    class Meta:
        model = Projetos
        fields = ['id', 'nome', 'email', 'descricao', 'usuario', 'habilidades']