from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from .Palavra import Palavra
from .Perfil import Perfil
from unidecode import unidecode
import re


class Partida(models.Model):
    jogador = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    palavra = models.ForeignKey(Palavra, on_delete=models.CASCADE)
    sessao = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    inicio = models.DateTimeField('Início da partida', auto_now_add=True)
    ultimo_acesso = models.DateTimeField('Última vez que o jogador jogou a partida', auto_now=True)
    errou = models.SmallIntegerField('Quantas vezes o jogador errou as letras', default=0)
    letras = models.CharField('Letras que foram jogadas', max_length=26)
    ganhou = models.BooleanField(null=True)

    def adivinhar_letra(self, letra):

        if letra in self.letras or not letra.isalpha() or len(letra) != 1 or self.ganhou is not None:
            return

        if letra not in self.palavra_normalizada():
            self.errou += 1

        self.letras += letra

        self.contabilizar_inicio_partida_perfil()

        if self.errou >= 6:
            self.perdeu()
        elif '_' not in self.palavra_descoberta:
            self.venceu()

    def adivinhar_palavra(self, palavra):

        palavra = self.normalizar_texto(palavra)

        if palavra == '' or self.ganhou is not None:
            return

        self.contabilizar_inicio_partida_perfil()

        if palavra == self.palavra_normalizada():
            self.venceu()
        else:
            self.perdeu()

    def get_letras_utilizadas(self):

      return list(self.letras)

    def venceu(self):

        self.ganhou = True
        self.contabilizar_partida_no_perfil()

    def perdeu(self):

        self.ganhou = False
        self.contabilizar_partida_no_perfil()

    def criar_perfil(self):

        perfil = Perfil(usuario=self.jogador)
        perfil.save()
        return perfil

    def contabilizar_inicio_partida_perfil(self):

        if len(self.letras) is 1:
            perfil = self.perfil_do_jogador()

            if perfil is not None:
                perfil.jogos += 1
                perfil.save()

    def contabilizar_partida_no_perfil(self):

        perfil = self.perfil_do_jogador()

        if perfil:
            if self.ganhou:
                perfil.venceu += 1
            else:
                perfil.perdeu += 1
            perfil.save()

    def perfil_do_jogador(self):
        if self.jogador is None:
            return None

        perfil = Perfil.objects.filter(usuario=self.jogador).first()

        if perfil is None:
            return self.criar_perfil()
        return perfil

    @property
    def palavra_descoberta(self):

        palavra_original = self.palavra.descricao
        sem_pontuacao_palavra = re.sub('[^%s_\-0-9]' % self.letras, '_', unidecode(palavra_original.lower()))
        letras_palavra = list(sem_pontuacao_palavra)

        for indice, letra in enumerate(letras_palavra):
            if letra != '_':
                letras_palavra[indice] = palavra_original[indice]

        return str.join('', letras_palavra)

    def palavra_normalizada(self):
        return self.normalizar_texto(self.palavra.descricao)

    @staticmethod
    def normalizar_texto(texto):
        return unidecode(texto.strip().lower())

    @classmethod
    def criar_randomica(cls, usuario, sessao):

        from random import randint

        total = Palavra.objects.count()
        palavra_selecionada = Palavra.objects.all()[randint(0, total - 1)]

        sessao_encontrada = Session.objects.filter(session_key=sessao.session_key).first()

        if usuario is not None:
            perfil_encontrado = Perfil.objects.filter(usuario=usuario).first()
            if perfil_encontrado is None:
                perfil = Perfil(usuario=usuario)
                perfil.save()

        return cls(jogador=usuario, palavra=palavra_selecionada, sessao=sessao_encontrada)

    def __str__(self):
        return 'jogador {0}, palavra: {1}, quantidade de tentativas que errou: {2}, id: {3}'.format(self.jogador, self.palavra.descricao, self.errou, self.id)

    def save(self):
        self.letras = str.join('', sorted(self.get_letras_utilizadas()))
        super().save()