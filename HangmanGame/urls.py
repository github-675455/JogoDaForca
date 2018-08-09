from django.urls import path
from .views.Jogo import Jogo
from .views.Home import Home

app_name = 'HangmanGame'

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('iniciar', Jogo.as_view(), name="iniciar"),
]
