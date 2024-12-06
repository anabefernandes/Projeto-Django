from django.db import models

# Create your models here.

class Usuario(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)
    foto = models.ImageField(upload_to='imagens/')

class Curso(models.Model):
    nome_curso = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    duracao = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    foto = models.ImageField(upload_to='imagens/', blank=True, null=True)
    estoque = models.PositiveIntegerField(default=0)  # Defina o estoque com valor padrão (0)

    def reduzir_estoque(self):
        if self.estoque >= 1:
            self.estoque -= 1
            self.save()
        else:
            raise ValueError("Estoque insuficiente")


class Foto(models.Model):
    nome = models.CharField(max_length=255)
    foto = models.ImageField(upload_to='imagens/')

class Contato(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mensagem = models.TextField(max_length=400)

class Venda(models.Model):
    id_curso = models.IntegerField() 
    nome_curso = models.CharField(max_length=255)  
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)  
    data_venda = models.DateTimeField(auto_now_add=True)
    

