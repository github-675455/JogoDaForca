from django.views.generic import View
from django.shortcuts import render

class Home(View):

    def get(self, request):
        return render(request, 'HangmanGame/index.html', {'continuar_jogo': bool(request.session.get('palavra') != None)})
