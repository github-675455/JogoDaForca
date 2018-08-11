from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    jogos = models.IntegerField(default=0)
    perdeu = models.IntegerField(default=0)
    venceu = models.IntegerField(default=0)

    def __str__(self):
        return 'perfil de %s' % self.usuario.get_username();