# Generated by Django 5.1.3 on 2024-12-01 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_contato'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='estoque',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
