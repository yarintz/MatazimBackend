# Generated by Django 3.2.8 on 2021-12-26 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_class'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(to='main.UserProfile'),
        ),
    ]
