from django.shortcuts import render, redirect
from .forms import ConfigForm, JogadoresForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlencode
from django.views.generic import View

def home(request):
    return render(request, 'index.html')

class ConfigView(View):
    def get(self, request, *args, **kwargs):
        form = ConfigForm()
        return render(request, "config.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = ConfigForm(request.POST)
        if form.is_valid():
            numero = form.cleaned_data["numero"]
            return redirect("jogadores", numero=numero)
        return render(request, "config.html", {"form": form})


class JogadoresView(View):
    def get(self, request, numero, *args, **kwargs):
        form = JogadoresForm(numero=numero)
        return render(request, "jogadores.html", {"form": form, "numero": numero})

    def post(self, request, numero, *args, **kwargs):
        form = JogadoresForm(request.POST, numero=numero)
        if form.is_valid():
            jogadores = [form.cleaned_data[f"jogador_{i}"] for i in range(1, numero + 1)]
            request.session['jogadores'] = jogadores
            return redirect("chaveamento")
        return render(request, "jogadores.html", {"form": form, "numero": numero})

class ChaveamentoView(View):
    template_name = 'chaveamento.html'

    def get(self, request, *args, **kwargs):
        jogadores = request.session.get('jogadores', [])
        partidas = [(jogadores[i], jogadores[i + 1]) for i in range(0, len(jogadores), 2)]
        return render(request, self.template_name, {'rodada': 1, 'partidas': partidas})

    def post(self, request, *args, **kwargs):
        vencedores = []
        for i in range(1, len(request.POST)):
            vencedor = request.POST.get(f'vencedor_{i}')
            if vencedor:
                vencedores.append(vencedor)

        if len(vencedores) == 1:  
            return render(request, 'resultado.html', {'campeao': vencedores[0]})

        novas_partidas = [(vencedores[i], vencedores[i + 1]) for i in range(0, len(vencedores), 2)]
        rodada = int(request.POST.get('rodada', 1)) + 1

        return render(request, self.template_name, {'rodada': rodada, 'partidas': novas_partidas})
    

def loginpage(request):
    return render(request, 'login.html')


def registerpage(request):
    return render(request, 'cadastro.html')
