# Generated by Django 3.1.3 on 2020-11-11 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1000)),
                ('nodes', models.IntegerField()),
            ],
        ),
    ]
