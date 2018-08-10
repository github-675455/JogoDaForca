from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import requires_csrf_token
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from ..models import Palavra, Partida

class Jogo(View):

    def get(self, request):

        partida_id = request.GET.get('partida')

        partida_id = partida_id if partida_id else request.session.get('partida-id')

        nova_partida = request.GET.get('novo')

        usuario = request.user if request.user.is_authenticated else None

        if partida_id != None and not nova_partida:
            partida = Partida.objects.get(pk=partida_id)
        else:
            partida = Partida.criar(usuario=usuario)
            partida.save()
            request.session['partida-id'] = partida.id

        context = {
            'partida': partida,
        }

        return render(request, 'HangmanGame/jogo.html', context)

    def post(self, request):
        partida_id = request.POST.get('partida-id')

        partida_encontrada = Partida.objects.get(pk=partida_id)

        if partida_encontrada.jogador != None:

            usuario_autenticado = request.user

            if usuario_autenticado != partida_encontrada.jogador:
                return HttpResponse(status=401)



        tentativa_letra = request.POST.get('tentativa-letra')
        tentativa_palavra = request.POST.get('tentativa-palavra')

        if tentativa_letra == None:
            return HttpResponse(status=500)

        tentativa_letra = tentativa_letra[0]

        partida_encontrada.incluir_letra_tentada(letra=tentativa_letra)

        partida_encontrada.save()

        return render(request, 'HangmanGame/jogo.html', {'partida': partida_encontrada})