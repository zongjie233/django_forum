# Generated by Django 3.1.2 on 2020-10-26 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='last_updated',
            field=models.DateField(auto_now_add=True),
        ),
    ]
