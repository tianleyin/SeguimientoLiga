# Generated by Django 4.2 on 2024-03-01 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lliga', '0002_partido_detalles_partido_inicio_partido_liga_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fitxa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jugador', models.CharField(max_length=100)),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lliga.equipo')),
            ],
        ),
    ]
