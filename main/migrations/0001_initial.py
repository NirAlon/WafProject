# Generated by Django 3.1.4 on 2021-02-13 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Logger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('threshold', models.IntegerField()),
                ('type_attack', models.CharField(max_length=255)),
                ('command', models.CharField(max_length=1024)),
                ('if_warn', models.BooleanField()),
            ],
        ),
    ]
