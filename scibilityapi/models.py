# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.conf import settings
from django.db import models


class Habilidades(models.Model):
    nome = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'habilidades'

class Usuario(models.Model):
    descricao = models.TextField(blank=True, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='usuario')
    habilidades = models.ManyToManyField(Habilidades, through='HabilidadesUsuario')
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    class Meta:
        managed = True
        db_table = 'usuario'

class Projetos(models.Model):
    nome = models.CharField(max_length=50)
    email = models.EmailField()
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projeto_usuario')
    habilidades = models.ManyToManyField(Habilidades, through='HabilidadesProjeto')
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'projetos'
        
class HabilidadesProjeto(models.Model):
    projeto = models.ForeignKey('Projetos', on_delete=models.CASCADE)  # The composite primary key (projeto_id, habilidade_id) found, that is not supported. The first column is selected.
    habilidade = models.ForeignKey('Habilidades', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'habilidades_projeto'
        unique_together = (('projeto', 'habilidade'),)


class HabilidadesUsuario(models.Model):
    pessoa = models.ForeignKey('Usuario', on_delete=models.CASCADE)  # The composite primary key (pessoa_id, habilidade_id) found, that is not supported. The first column is selected.
    habilidade = models.ForeignKey('Habilidades', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'habilidades_usuario'
        unique_together = (('pessoa', 'habilidade'),)




