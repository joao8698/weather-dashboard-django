from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.login_user, name='login_user'),
    path('cadastrar/', views.cadastro, name='cadastro'),
    path('pesquisar/clima/', views.clima, name='clima'),
    path('pesquisar/', views.pesquisar, name='pesquisar'),
    path('', views.base_page, name='base-page'),
]