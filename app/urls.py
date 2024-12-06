from django.urls import path
from . import views

urlpatterns = [
    path('', views.app, name="app"),
    path('login/', views.fazerlogin, name="fazerlogin"),
    path('cadastro/', views.cadastrar_user, name="cadastrar_user"),
    path('usuarios/', views.exibir_user, name="exibir_user"),
    path('cursos/', views.exibir_curso, name="exibir_curso"),
    path('cadastro_curso/', views.cadastrar_curso, name="cadastrar_curso"),
    path('editar_usuario/<int:id_usuario>/', views.editar_usuario, name="editar_usuario"),
    path('excluir_usuario/<int:id_usuario>/', views.excluir_usuario, name="excluir_usuario"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('alterar_senha/', views.alterar_senha, name="alterar_senha"),
    path('excluir_conta/', views.excluir_conta, name="excluir_conta"),
    path('logout/', views.userLogout, name="logout"),
    path('add-foto/', views.add_foto, name="add_foto"),
    path('galeria/', views.galeria, name="galeria"),
    path('excluir_curso/<int:id_curso>/', views.excluir_curso, name="excluir_curso"),
    path('comprar/<int:id_curso>/', views.realizar_venda, name="realizar_venda"),
    path('contato/', views.contato, name="contato"),
    path('relatorio_vendas/', views.relatorio_vendas, name='relatorio_vendas'),

]
