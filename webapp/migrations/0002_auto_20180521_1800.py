# Generated by Django 2.0.5 on 2018-05-21 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='isbn',
            field=models.BigIntegerField(primary_key='true', serialize=False),
        ),
    ]
