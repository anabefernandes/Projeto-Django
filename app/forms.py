from django import forms
from app.models import Usuario, Curso, Foto, Contato

class FormCadastroUser(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nome','email','senha','foto')
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome', 'class': 'form-control' }),
            'email': forms.EmailInput(attrs={'placeholder': 'usuario@email.com', 'class': 'form-control' }),
            'senha': forms.PasswordInput(attrs={'placeholder': 'Senha', 'class': 'form-control' }),
            'foto': forms.FileInput(attrs={'accept':'image/*'})
        }

class FormCadastroCurso(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ('nome_curso','autor','duracao', 'preco', 'foto', 'estoque')
        widgets = {
            'nome_curso': forms.TextInput(attrs={'placeholder': 'Nome do Projeto', 'class': 'form-control' }),
            'autor': forms.TextInput(attrs={'placeholder': 'Nome do autor', 'class': 'form-control' }),
            'duracao': forms.NumberInput(attrs={'placeholder': 'Duração em horas', 'class': 'form-control' }),
            'preco': forms.NumberInput(attrs={'step':'0.01', 'placeholder': 'Preço em R$', 'class': 'form-control' }),
            'estoque': forms.TextInput(attrs={'placeholder': 'Quantidade em estoque', 'class': 'form-control' }),
            'foto': forms.FileInput(attrs={'accept':'image/*'})

        }

class FormLogin(forms.ModelForm):

    class Meta:
        model = Usuario 
        fields = ('email', 'senha')
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'usuario@email.com', 'class': 'form-control' }),
            'senha': forms.PasswordInput(attrs={'class': 'form-control border border-success', 'type': 'password' }),        
            }
        
class FormFoto(forms.ModelForm):
    class Meta:
        model = Foto
        fields = ['nome','foto']

        widgets = {
            'foto': forms.FileInput(attrs={'accept':'image/*'})
        }

class FormContato(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'email', 'mensagem']
        widgets = {
                    'nome': forms.TextInput(attrs={'placeholder': 'Nome Completo', 'class': 'form-control' }),
                    'email': forms.EmailInput(attrs={'placeholder': 'usuario@email.com', 'class': 'form-control' }),
                    'mensagem': forms.Textarea(attrs={'placeholder': 'Escreva aqui sua mensagem', 'class': 'form-control' }),
        }