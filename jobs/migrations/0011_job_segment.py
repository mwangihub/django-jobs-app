# Generated by Django 3.0 on 2021-11-02 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0010_auto_20211031_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='segment',
            field=models.CharField(default='create-job', editable=False, max_length=10),
        ),
    ]
