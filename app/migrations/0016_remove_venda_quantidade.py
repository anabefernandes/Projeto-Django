# Generated by Django 5.1.2 on 2024-12-06 00:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_venda_quantidade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venda',
            name='quantidade',
        ),
    ]
