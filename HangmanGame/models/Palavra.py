from django.db import models
from django.contrib.auth.models import User
import re


class Palavra(models.Model):
    descricao = models.CharField('Descrição da palavra', max_length=254, unique=True)
    comentario = models.TextField('Comentário, informações adicionais', blank=True)
    registrado = models.DateField('Data de registro', auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def mostrar_letras_encontradas(self, letras = []):
        """Esconde letras com '_', caso a letra não esteja no parametro de array letras

        Retorna por exemplo: Para a palavra "Tempo", caso tenha passado o valor ['e', 'o'], o resultado será "_emp_".

        """
        return re.sub('[^%s\s\-]' % ''.join(letras), '_', self.descricao)

    def __str__(self):
        return self.descricao