# Generated by Django 3.2.24 on 2024-03-05 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizkhalifa', '0002_auto_20240305_1111'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('options_text', models.TextField()),
                ('answer_text', models.CharField(max_length=255)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_information', to='quizkhalifa.game')),
            ],
        ),
    ]
