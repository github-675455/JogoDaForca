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

        palavra = self.palavra.descricao

        if letra in self.letras or self.ganhou != None:
            return

        if letra not in unidecode(palavra.lower()):
            self.errou += 1;

        self.letras += letra

        if self.errou >= 6:
            self.ganhou = False

        if '_' not in self.palavra_descoberta:
            self.ganhou = True

    def get_letras_utilizadas(self):
      return list(self.letras)

    @property
    def palavra_descoberta(self):

        palavra_original = self.palavra.descricao
        sem_pontuacao_palavra = re.sub('[^%s\_\-0-9]' % self.letras, '_', unidecode(palavra_original.lower()))
        letras_palavra = list(sem_pontuacao_palavra)

        for indice, letra in enumerate(letras_palavra):
            if letra != '_':
                letras_palavra[indice] = palavra_original[indice]

        return str.join('', letras_palavra)

    @classmethod
    def criar(cls, usuario):

        from random import randint

        total = Palavra.objects.count()
        palavra_selecionada = Palavra.objects.all()[randint(0, total - 1)]
        return cls(jogador=usuario, palavra=palavra_selecionada)

    def __str__(self):
        return 'jogador {0}, palavra: {1}, quantidade de tentativas que errou: {2}, id: {3}'.format(self.jogador, self.palavra.descricao, self.errou, self.id)

    def save(self, *args, **kwargs):
        self.letras = str.join('', sorted(self.get_letras_utilizadas()))
        super().save(*args, **kwargs)