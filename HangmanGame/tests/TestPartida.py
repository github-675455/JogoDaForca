from django.test import TestCase
from django.contrib.auth.models import User
from ..models.Partida import Partida
from ..models.Palavra import Palavra
from ..models.Perfil import Perfil


class TestPartida(TestCase):

    partida_test = None
    palavraDescricao = "test"

    def setUp(self):

        palavra = Palavra(descricao=self.palavraDescricao)
        palavra.save()
        usuario = User(username="test_user", password="12345")
        usuario.save()
        partida_test = Partida(jogador=usuario, palavra=palavra)
        partida_test.save()
        self.partida_test = partida_test

    def test_acertou_letra_na_palavra(self):

        self.partida_test.adivinhar_letra('t')
        self.assertTrue(self.partida_test.errou == 0,
                         "Usuário acertou a letra, mas foi contabilizado como letra errada na partida.")
        self.assertTrue(self.partida_test.ganhou == None,
                         "A partida não acabou ainda.")
        self.assertTrue(self.partida_test.jogador != None,
                         "A partida foi criada por um usuário cadastrado.")

    def test_acertou_palavra(self):

        self.partida_test.adivinhar_palavra(self.palavraDescricao)
        self.partida_test.save()
        self.assertTrue(self.partida_test.ganhou == True,
                        "O jogador ganhou partida, mas não foi salvo como partida ganha.")
        self.assertTrue(self.partida_test.errou == 0,
                         "Usuário acertou a palavra, mas foi contabilizado como letra errada na partida.")
        perfil_encontrado = Perfil.objects.filter(usuario_id=self.partida_test.jogador.id).first()
        self.assertTrue(perfil_encontrado != None, "O perfil do jogado não existe.")
        self.assertTrue(perfil_encontrado.venceu == 1, "O perfil do jogado não foi contabilizado.")
        self.assertTrue(perfil_encontrado.perdeu == 0, "O usuário ganhou, mas foi contabilizado como perda.")

    def test_contabiliza_total_partidas(self):

        self.partida_test.contabilizar_inicio_partida_perfil()
        self.partida_test.save()
        perfil_encontrado = Perfil.objects.filter(usuario_id=self.partida_test.jogador.id).first()
        self.assertTrue(perfil_encontrado != None,
                        "O perfil do jogado não existe.")
        self.assertTrue(perfil_encontrado.jogos == 1,
                        "Não contabilizou a partida, no total de partidadas jogadas do perfil do usuário.")