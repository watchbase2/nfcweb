# Generated by Django 4.1.1 on 2022-09-10 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NFC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('snumber', models.CharField(max_length=20)),
                ('uid', models.CharField(max_length=40)),
                ('jan', models.CharField(max_length=13)),
            ],
        ),
    ]