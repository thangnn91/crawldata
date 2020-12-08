# Generated by Django 2.2.14 on 2020-10-06 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('price', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=500)),
                ('publish_date', models.CharField(max_length=15)),
                ('publisher', models.CharField(max_length=100)),
                ('publisher_mobile', models.CharField(max_length=15)),
                ('description', models.TextField()),
                ('square', models.CharField(max_length=20)),
                ('direction', models.CharField(max_length=50)),
                ('policy', models.CharField(max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'tbl_data',
            },
        ),
    ]