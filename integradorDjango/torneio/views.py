from django.shortcuts import render
from .models import Torneio

# Create your views here.

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
