# Generated by Django 3.0 on 2021-11-02 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20211031_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='innovestsubcribers',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
