from django.db import models
from django.contrib.auth.models import User
from .Palavra import Palavra
from unidecode import unidecode
import re

class Partida(models.Model):
    jogador = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    palavra = models.ForeignKey(Palavra, on_delete=models.CASCADE)
    inicio = models.DateTimeField('Início da partida', auto_now_add=True)
    ultimo_acesso = models.DateTimeField('Última vez que o jogador jogou a partida', auto_now=True)
    errou = models.SmallIntegerField('Quantas vezes o jogador errou as letras', default=0)
    letras = models.CharField('Letras que foram jogadas', max_length=26)
    ganhou = models.BooleanField(null=True)

    def incluir_letra_tentada(self, letra):
        self.letras += letra

    @property
    def get_letras_utilizadas(self):
        return list(self.letras)

    @property
    def palavra_descoberta(self):
        return re.sub('[^%s\_\-0-9]' %  self.letras, '_', unidecode(self.palavra.description))

    def __str__(self):
        return 'jogador %s, palavra: %s, qt tentativas que errou: %s' % self.jogador.get_username() % self.palavra.descricao % self.errou

    def save(self, *args, **kwargs):
        self.letras = str.join('', sorted(self.get_letras_utilizadas()))
        super().save(*args, **kwargs)