from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views.Jogo import Jogo

app_name = 'HangmanGame'

urlpatterns = [
    path('', Jogo.as_view(), name="home"),
    path('iniciar', Jogo.as_view(), name="iniciar"),
    path('continuar', Jogo.as_view(), name="continuar"),
    path('entrar', LoginView.as_view()),
    path('sair', LogoutView.as_view()),
]
