# Generated by Django 2.1 on 2018-08-09 04:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Palavra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=254, unique=True, verbose_name='Descrição da palavra')),
                ('comentario', models.TextField(verbose_name='Comentário, informações adicionais')),
                ('registrado', models.DateField(auto_now_add=True, verbose_name='Data de registro')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Partida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio', models.DateTimeField(auto_now_add=True, verbose_name='Início da partida')),
                ('ultimo_acesso', models.DateTimeField(auto_now=True, verbose_name='Última vez que o jogador jogou a partida')),
                ('errou', models.SmallIntegerField(default=0, verbose_name='Quantas vezes o jogador errou as letras')),
                ('letras', models.CharField(max_length=26, verbose_name='Letras que foram jogadas')),
                ('ganhou', models.BooleanField(null=True)),
                ('jogador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('palavra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HangmanGame.Palavra')),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jogos', models.IntegerField(default=0)),
                ('perdeu', models.IntegerField(default=0)),
                ('venceu', models.IntegerField(default=0)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]