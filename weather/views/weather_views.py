from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import geocoder
from utils.openweathermap_api import buscar_cidade, verificar_clima, API_KEY

print(API_KEY)

# Create your views here.

# ============================================================================================= #

def cadastro(request):
    if request.method == "GET":
        return render(request, 'main_templates/cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return HttpResponse('Já existe um usuário com esse nome!')
        
        if User.objects.filter(email=email).exists():
            return HttpResponse('Já existe um usuário com esse e-mail!')

        User.objects.create_user(username=username, email=email, password=password)

        return redirect('weather:login_user')
    
def login_user(request):
    if request.method == 'GET':
        return render(request, 'main_templates/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('weather:pesquisar')
        else:
            return render(request, 'main_templates/login.html')

def logout_user(request):
    logout(request)
    return redirect('weather:base-page')

def base_page(request):
    return render(request, 'partials/base.html')


@login_required(login_url='/login/')
def pesquisar(request):
    return render(request, 'main_templates/index.html')

@login_required(login_url='/login/')
def clima(request):
    cidade = request.GET.get('cidade')
    latitude = longitude = None

    LOCALIZACAO = geocoder.ip('me')
    LOCALIZACAO_PAIS = LOCALIZACAO.country

    if cidade:
        latitude, longitude = buscar_cidade(
            cidade,
            API_KEY,
            COUNTRY_CODE=LOCALIZACAO_PAIS
        )

        if latitude and longitude:
            dados = verificar_clima(latitude, longitude, API_KEY)
        else:
            dados = None
    else:
        dados = None

    print(dados)

    if dados:
        dados_do_clima = {
            'cidade': cidade.strip().title(),
            'coords': dados.get('coords'),
            'weather': dados.get('weather')[0] if dados.get('weather') else {},
            'main': dados.get('main'),
            'wind': dados.get('wind'),
        }
    else:
        dados_do_clima = {}

    print(dados)

    return render(request,
                'main_templates/clima.html',
                dados_do_clima,
                )