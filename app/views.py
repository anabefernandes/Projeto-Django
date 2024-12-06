from datetime import timezone
from django.shortcuts import get_object_or_404, render,redirect

#importa a funcao get_template() do módulo loader
from app.forms import FormCadastroUser, FormCadastroCurso, FormLogin, FormFoto, FormContato
from django.contrib import messages
from app.models import Usuario, Curso, Foto, Venda
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout

##Grafico
from django.shortcuts import render
import io
import urllib, base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.db.models import Sum, Count
from django.db.models.functions import TruncDay
from datetime import datetime
from django.utils import timezone  




def app(request):
    
    email_do_usuario = request.session.get('email')

    context = {
        'email_do_usuario': email_do_usuario,
     }
    return render(request, 'index.html', context)

def cadastrar_user(request):
    novo_user = FormCadastroUser(request.POST or None, request.FILES or None)
    
    # SALVAR USUÁRIO
    if request.method == 'POST':
        if novo_user.is_valid():
            usuario = novo_user.save(commit=False)  # Evita salvar imediatamente no banco
            # Criptografa a senha antes de salvar
            usuario.senha = make_password(novo_user.cleaned_data['senha'])
            usuario.save()  # Agora salva com a senha criptografada
            messages.success(request, "Usuário cadastrado com sucesso!")
            return redirect('app')  # Redireciona para a página principal ou de login
    
    context = {
        'form': novo_user
    }

    return render(request, 'cadastro.html', context)
from django.shortcuts import render, redirect
from django.contrib import messages
from app.forms import FormCadastroCurso  # Importando o FormCadastroCurso
from app.models import Curso

def cadastrar_curso(request):
    # Verifica se o usuário está autenticado
    if not request.session.get('email'):
        messages.error(request, "Faça seu login para cadastrar seu curso!")
        return redirect('fazerlogin')

    # Criação do formulário
    if request.method == 'POST':
        form = FormCadastroCurso(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Salva o curso no banco de dados
            messages.success(request, "Curso cadastrado com sucesso!")
            return redirect('exibir_curso')  # Redireciona para a página que exibe os cursos
    else:
        form = FormCadastroCurso()  # Formulário vazio para o método GET

    context = {'form': form}
    return render(request, 'cadastro_curso.html', context)


def exibir_user(request):
    usuarios = Usuario.objects.all()

    context = {
        'dados' : usuarios
    }

    return render(request, 'usuarios.html', context)

def exibir_curso(request):
    cursos = Curso.objects.all()

    context = {
        'cursos' : cursos
    }

    return render(request, 'cursos.html', context)

def dashboard(request):
    if not request.session.get('email'):
        return redirect('fazerlogin')

    email = request.session['email']
    usuario = Usuario.objects.get(email=email)

    context = {
        'usuario': usuario
    }
    
    return render(request, 'dashboard.html', context)

def fazerlogin(request):
    formL = FormLogin(request.POST or None)
    
    if request.method == 'POST':
        _email = request.POST.get('email')
        _senha = request.POST.get('senha')
        
        if not _email or not _senha:
            messages.error(request, 'Por favor, preencha todos os campos.')
            return render(request, 'login.html', {'formLogin': formL})

        try:
            usuarioL = Usuario.objects.get(email=_email)
            if check_password(_senha, usuarioL.senha):  
                request.session.set_expiry(3000)  # Sessão de 30 segundos
                request.session['email'] = _email
                request.session['nome'] = usuarioL.nome
                messages.success(request, 'Login bem-sucedido!')
                return redirect('dashboard')  # Redireciona para o dashboard
            else:
                messages.error(request, 'Credenciais inválidas. Por favor, tente novamente!')
        except Usuario.DoesNotExist:
            messages.error(request, 'Credenciais inválidas. Por favor, tente novamente!')

    return render(request, 'login.html', {'formLogin': formL})  # Certifique-se de que a variável formLogin está sendo passada


def editar_usuario(request, id_usuario):
    if not request.session.get('email'):
        messages.error(request, "Faça seu login para Editar ou Excluir contas!")
        return redirect('fazerlogin')

    usuario = Usuario.objects.get(id=id_usuario)
    form = FormCadastroUser(request.POST or None, instance=usuario)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('exibir_user')
    context = {
            'form' : form
        }
    return render(request, 'editar_usuario.html', context)

def excluir_usuario(request, id_usuario):
    if not request.session.get('email'):
        messages.error(request, "Faça seu login para Editar ou Excluir contas!")
        return redirect('fazerlogin')

    usuario = Usuario.objects.get(id=id_usuario)
    usuario.delete()
    return redirect('exibir_user')

def excluir_conta(request):
    if not request.session.get('email'):
        return redirect('fazerlogin')
    
    email = request.session['email']
    usuario = Usuario.objects.get(email=email)

    # Exclui o usuário
    usuario.delete()
    
    # Limpa a sessão do usuário
    request.session.flush()  
    
    # Redireciona para a página inicial
    messages.success(request, 'Conta excluída com sucesso.')
    return redirect('app')  # Ou o nome da sua página inicial

def alterar_senha(request):
    if not request.session.get('email'):
        return redirect('fazerlogin')

    if request.method == 'POST':
        email = request.session['email']
        usuario = Usuario.objects.get(email=email)
        
        senha_atual = request.POST.get('senha_atual')
        nova_senha = request.POST.get('nova_senha')
        confirmacao_senha = request.POST.get('confirmacao_senha')

        # Verifica se a senha atual está correta
        if not check_password(senha_atual, usuario.senha):
            messages.error(request, 'A senha atual está incorreta.')
            return render(request, 'alterar_senha.html')

        # Verifica se a nova senha e a confirmação coincidem
        if nova_senha != confirmacao_senha:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'alterar_senha.html')

        # Atualiza a senha
        usuario.senha = make_password(nova_senha)  # Criptografa a nova senha
        usuario.save()
        messages.success(request, 'Senha alterada com sucesso!')
        return redirect('dashboard')

    return render(request, 'alterar_senha.html')

def add_foto(request):
    if request.method == 'POST':
        form = FormFoto(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('galeria')
    else:
        form = FormFoto()
    return render (request, 'add_foto.html', {'form': form})

def galeria(request):
    # Buscando as fotos de cada modelo
    usuarios_fotos = Usuario.objects.all()
    cursos_fotos = Curso.objects.all()
    fotos_fotos = Foto.objects.all()

    # Passando as fotos para o contexto
    context = {
        'usuarios_fotos': usuarios_fotos,
        'cursos_fotos': cursos_fotos,
        'fotos_fotos': fotos_fotos,
    }
    
    return render(request, 'galeria.html', context)

def excluir_curso(request, id_curso):
    curso = Curso.objects.get(id=id_curso)
    curso.delete()
    return redirect('exibir_curso')

def contato(request):
    novo_contato = FormContato(request.POST or None)
    
    # SALVAR USUÁRIO
    if request.method == 'POST':
        if novo_contato.is_valid():
            contato = novo_contato.save(commit=True)
            messages.success(request, "Mensagem enviada com sucesso!")
            return redirect('app')  # Redireciona para a página principal ou de login
    
    context = {
        'form': novo_contato
    }

    return render(request, 'contato.html', context)

def userLogout (request):

    logout(request)
    messages.success(request, 'A sessao foi encerrada!')
    return redirect('app')

def realizar_venda(request, id_curso):
    # Recupera o curso com base no ID
    curso = get_object_or_404(Curso, id=id_curso)
    
    try:
        # Reduz o estoque do curso
        curso.reduzir_estoque()

        # Cria o registro da venda
        Venda.objects.create(
            id_curso=curso.id, 
            nome_curso=curso.nome_curso, 
            valor_total=curso.preco * 1  
        )

        messages.success(request, "Compra realizada com sucesso!")
        return redirect('exibir_curso')  
    except ValueError as e:
        # Lida com erros, como estoque insuficiente
        messages.error(request, str(e))
        return redirect('exibir_curso')

def relatorio_vendas(request):
    hoje = timezone.now()
    mes_atual = hoje.month
    ano_atual = hoje.year
 
    vendas_gerais = Venda.objects.filter(data_venda__month=mes_atual, data_venda__year=ano_atual).values('data_venda__month').annotate(total_vendas=Count('id'))
 
    meses = [venda['data_venda__month'] for venda in vendas_gerais]
    total_vendas = [venda['total_vendas'] for venda in vendas_gerais]
 
    fig_gerais, ax_gerais = plt.subplots()
    ax_gerais.bar(meses, total_vendas, label="Vendas Totais", color='blue')
    ax_gerais.set_title("Vendas Gerais Mensais")
    ax_gerais.set_xlabel("Mês")
    ax_gerais.set_ylabel("Quantidade de Vendas")
    ax_gerais.set_xticks(range(1, 13))  
    ax_gerais.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax_gerais.legend()
 
    buf_gerais = io.BytesIO()
    fig_gerais.savefig(buf_gerais, format='png')
    buf_gerais.seek(0)
    img_gerais = base64.b64encode(buf_gerais.getvalue()).decode('utf-8')
 
    vendas_por_curso = Venda.objects.filter(data_venda__month=mes_atual, data_venda__year=ano_atual).values('nome_curso').annotate(total_vendas=Count('id'))
 
    cursos = [venda['nome_curso'] for venda in vendas_por_curso]
    vendas_por_curso_vals = [venda['total_vendas'] for venda in vendas_por_curso]
 
    fig_curso, ax_curso = plt.subplots()
    ax_curso.bar(cursos, vendas_por_curso_vals, color='green')
    ax_curso.set_title("Vendas por Curso")
    ax_curso.set_xlabel("Curso")
    ax_curso.set_ylabel("Quantidade de Vendas")
 
    buf_curso = io.BytesIO()
    fig_curso.savefig(buf_curso, format='png')
    buf_curso.seek(0)
    img_curso = base64.b64encode(buf_curso.getvalue()).decode('utf-8')
 
    context = {
        'vendas_gerais': vendas_gerais,
        'vendas_por_curso': vendas_por_curso,
        'img_gerais': img_gerais,
        'img_curso': img_curso,
    }
    return render(request, 'relatorio_vendas.html', context)