""" from django.db import models

class Project(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    descricao = models.TextField()
    
class Hability(models.Model):
    nome = models.CharField(max_length=255)

class ProjectHability(models.Model):
    projeto = models.ForeignKey(Project, on_delete=models.PROTECT)
    habilidade = models.ForeignKey(Hability, on_delete=models.CASCADE)
    
class User(models.Model):
    nome =  models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)
    descricao = models.TextField()       """