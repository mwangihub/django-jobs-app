# Generated by Django 3.2 on 2021-11-13 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_rename_themes_theme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, null=True),
        ),
    ]