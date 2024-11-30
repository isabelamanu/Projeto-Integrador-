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

class QuantidadeJogadoresView(View):
    template_name = "numero_jogadores.html"

    def post(self, request, *args, **kwargs):
        numero = int(request.POST.get('numero'))
        return render(request, 'adicionar_jogadores.html', {'numero': numero})
    


