from scibilityapi.models import HabilidadesUsuario, Projetos, Habilidades, HabilidadesProjeto, Usuario, InteresseProjeto
from rest_framework import serializers

        
class HabilidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habilidades
        fields = ['id', 'nome']

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
    projetos_interessados = serializers.SerializerMethodField()
    
    class Meta:
        model = Usuario
        fields = ['id', 'user_id', 'nome_completo', 'descricao', 'projetos', 'habilidades', 'projetos_interessados']
        
    def get_nome_completo(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'
    
    def get_projetos_interessados(self, obj):
        # Obtendo os projetos pelos quais o usuário demonstrou interesse
        interesses = InteresseProjeto.objects.filter(usuario=obj).select_related('projeto')
        return ProjetoSimplesSerializer([interesse.projeto for interesse in interesses], many=True).data
        
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
        
class InteresseProjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteresseProjeto
        fields = ['id', 'usuario', 'projeto']
        
    def create(self, validated_data):
        # Garantir que o interesse não seja duplicado
        interesse, created = InteresseProjeto.objects.get_or_create(**validated_data)
        return interesse