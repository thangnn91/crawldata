# Generated by Django 2.2.14 on 2020-10-09 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0005_logcrawl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='systemconfig',
            name='param_page',
        ),
        migrations.RemoveField(
            model_name='systemconfig',
            name='source',
        ),
        migrations.AddField(
            model_name='systemconfig',
            name='city',
            field=models.CharField(default='SOME STRING', max_length=50),
        ),
        migrations.AddField(
            model_name='systemconfig',
            name='district',
            field=models.CharField(default='SOME STRING', max_length=50),
        ),
    ]
