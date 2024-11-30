from django.shortcuts import render, redirect
from django.http import HttpResponse

def home_page(request):
    context = {'title': 'Pagina Principal', 'content':'principal'}
    return render(request, 'index.html')

def pagina_cadastro(request):
    return render(request, 'cadastro.html')

def chaveamento(request):
    return render(request, 'chaveamento.html')