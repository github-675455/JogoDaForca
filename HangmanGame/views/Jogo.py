from django.views.decorators.cache import cache_page
from django.views.generic import View
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from ..models import Palavra


class Jogo(View):

    def get(self, request):
        from random import randint

        palavra_selecionada = None

        continuar_jogo = request.GET.get('continuar');

        if(continuar_jogo != None):
            palavra_selecionada = Palavra.objects.get(pk=request.session['palavra'])
        else:
            total = Palavra.objects.count()
            palavra_selecionada = Palavra.objects.all()[randint(0, total - 1)]
            request.session['palavra'] = palavra_selecionada.id

        template = loader.get_template('HangmanGame/index.html')
        context = {
            'palavra_selecionada': palavra_selecionada,
        }
        return HttpResponse(template.render(context))