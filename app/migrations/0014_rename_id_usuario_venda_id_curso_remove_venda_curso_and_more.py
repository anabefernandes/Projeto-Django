# Generated by Django 5.1.2 on 2024-12-05 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_remove_venda_usuario_venda_id_usuario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='venda',
            old_name='id_usuario',
            new_name='id_curso',
        ),
        migrations.RemoveField(
            model_name='venda',
            name='curso',
        ),
        migrations.RemoveField(
            model_name='venda',
            name='quantidade',
        ),
        migrations.AddField(
            model_name='venda',
            name='nome_curso',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]
