# Generated by Django 3.2.4 on 2021-06-15 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dynamic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compensation', models.CharField(max_length=10)),
                ('instructions', models.TextField()),
                ('preconnect1', models.TextField()),
                ('preconnect2', models.TextField()),
                ('thankyou_code', models.CharField(max_length=20)),
            ],
        ),
    ]