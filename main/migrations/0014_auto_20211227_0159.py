# Generated by Django 3.2.8 on 2021-12-26 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20211226_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='coordinators',
            field=models.ManyToManyField(related_name='CoordinatorClasses', to='main.UserProfile'),
        ),
        migrations.AddField(
            model_name='class',
            name='teachers',
            field=models.ManyToManyField(related_name='TeacherClasses', to='main.UserProfile'),
        ),
        migrations.AlterField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(related_name='StudentClasses', to='main.UserProfile'),
        ),
    ]