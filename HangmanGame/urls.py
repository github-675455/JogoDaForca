from django.urls import path
from .views.Jogo import Jogo

app_name = 'HangmanGame'

urlpatterns = [
    path('', Jogo.as_view(), name="home"),
    path('iniciar', Jogo.as_view(), name="iniciar"),
    path('continuar', Jogo.as_view(), name="continuar"),
]
