# Generated by Django 5.0.2 on 2024-02-26 15:59

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("userID", models.AutoField(primary_key=True, serialize=False)),
                ("username", models.TextField(blank=True)),
                ("email", models.TextField(blank=True)),
                ("password", models.TextField()),
            ],
        ),
    ]
