# Generated by Django 3.2 on 2021-11-06 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        ('accounts', '0017_themes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='themes',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='session_theme', to='sessions.session'),
        ),
    ]
