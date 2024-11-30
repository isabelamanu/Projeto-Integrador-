from django.views.generic import TemplateView, FormView, View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Torneio

# Create your views here.
'''
FBV (function based view)
prefiro class based view, mas sao a mesma coisa

def quantidade_jogadores(request):
    if request.method == 'POST':
        numero = int(request.POST.get('numero'))
        return render(request, 'adicionar_jogadores.html', {'numero':numero})
    


def home_page(request):
    context = {'title': 'Pagina Principal', 'content':'principal'}
    return render(request, 'index.html')

def pagina_cadastro(request):
    return render(request, 'cadastro.html')

def chaveamento(request):
    return render(request, 'chaveamento.html')
'''

# CBV (class based view)

class QuantidadeJogadoresView(TemplateView):
    template_name = "numero_jogadores.html"

    def post(self, request, *args, **kwargs):
        numero = int(request.POST.get('numero'))
        return render(request, 'adicionar_jogadores.html', {'numero': numero})
    

class AdicionarJogadoresView(View):
    template_name = 'adicionar_jogadores.html'

    def post(self, request, *args, **kwargs):
        jogadores = request.POST.getlist('jogadores[]')
        quantidade_jogadores = len(jogadores)

        if (quantidade_jogadores & (quantidade_jogadores-1)) != 0:
            return render(request, self.template_name, {'error': 'O numero de jogadores deve ser uma potencia de 2', 'numero': quantidade_jogadores})

        rodadas = []
        rodadas.append(jogadores)
        while len(jogadores)>1:
            jogadores = ['']* (len(jogadores)//2)
            rodadas.append(jogadores)
        
        torneio, created = Torneio.objects.get_or_create(id=1)
        torneio.jogadores = rodadas[0]
        torneio.rodadas = rodadas
        torneio.campeao = ''
        torneio.save()

        return redirect('index')
        
