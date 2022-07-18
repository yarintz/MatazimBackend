# Generated by Django 3.2.8 on 2022-04-26 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20220322_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='matazes',
            field=models.ManyToManyField(related_name='matatzesClasses', to='main.UserProfile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='userType',
            field=models.CharField(choices=[('1', 'student'), ('2', 'matatz'), ('3', 'teacher'), ('4', 'coordinator'), ('5', 'admin')], default='1', max_length=20),
        ),
    ]