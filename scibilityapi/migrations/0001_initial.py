# Generated by Django 5.0.4 on 2024-04-15 23:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Habilidades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'habilidades',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='HabilidadesProjeto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('habilidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scibilityapi.habilidades')),
            ],
            options={
                'db_table': 'habilidades_projeto',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='HabilidadesUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('habilidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scibilityapi.habilidades')),
            ],
            options={
                'db_table': 'habilidades_usuario',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Projetos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('habilidades', models.ManyToManyField(through='scibilityapi.HabilidadesProjeto', to='scibilityapi.habilidades')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projeto_usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'projetos',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='habilidadesprojeto',
            name='projeto',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scibilityapi.projetos'),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField(blank=True, null=True)),
                ('habilidades', models.ManyToManyField(through='scibilityapi.HabilidadesUsuario', to='scibilityapi.habilidades')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'usuario',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='habilidadesusuario',
            name='pessoa',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scibilityapi.usuario'),
        ),
        migrations.AlterUniqueTogether(
            name='habilidadesprojeto',
            unique_together={('projeto', 'habilidade')},
        ),
        migrations.AlterUniqueTogether(
            name='habilidadesusuario',
            unique_together={('pessoa', 'habilidade')},
        ),
    ]
