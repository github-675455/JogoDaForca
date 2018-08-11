from django.views.decorators.cache import cache_page
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render
from ..models import Partida

class Jogo(View):

    def get(self, request):

        partida_id = request.GET.get('partida')

        partida_id = partida_id if partida_id else request.session.get('partida-id')

        nova_partida = request.GET.get('novo')

        usuario = request.user if request.user.is_authenticated else None

        if partida_id != None and not nova_partida:
            partida = Partida.objects.get(pk=partida_id)
        else:
            partida = Partida.criar_randomica(usuario=usuario)
            partida.save()
            request.session['partida-id'] = partida.id

        context = {
            'partida': partida,
        }

        return render(request, 'HangmanGame/jogo.html', context)

    def post(self, request):
        partida_id = request.POST.get('partida-id')

        partida_id = partida_id if partida_id is not '' else request.session.get('partida-id')

        if partida_id is not '':
            partida_encontrada = Partida.objects.filter(pk=partida_id).first()

            if partida_encontrada.jogador != None:

                usuario_autenticado = request.user

                if usuario_autenticado != partida_encontrada.jogador:
                    return HttpResponse(status=401)

        tentativa_letra = request.POST.get('tentativa-letra')
        tentativa_palavra = request.POST.get('tentativa-palavra')

        if tentativa_letra == '' and tentativa_palavra == '':
            return render(request, 'HangmanGame/jogo.html', {'partida': partida_encontrada})


        partida_encontrada.adivinhar_letra(letra=tentativa_letra[:1])

        partida_encontrada.adivinhar_palavra(palavra=tentativa_palavra)

        partida_encontrada.save()

        return render(request, 'HangmanGame/jogo.html', {'partida': partida_encontrada})