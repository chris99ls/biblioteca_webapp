# Generated by Django 2.0.5 on 2018-06-06 15:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GiaVisto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('books', models.ManyToManyField(to='webapp.Libro')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Prenotato',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('books', models.ManyToManyField(to='webapp.Libro')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
