# Generated by Django 3.2.4 on 2021-06-12 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fname',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('race', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Lname',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=200)),
                ('race', models.CharField(max_length=200)),
            ],
        ),
    ]