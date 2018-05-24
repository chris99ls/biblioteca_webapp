# Generated by Django 2.0.5 on 2018-05-21 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Libro',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('subject', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000)),
                ('tumbnail', models.CharField(max_length=200)),
                ('isbn', models.IntegerField(primary_key='true', serialize=False)),
            ],
        ),
    ]
