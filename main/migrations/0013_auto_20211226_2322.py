# Generated by Django 3.2.8 on 2021-12-26 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_class_students'),
    ]

    operations = [
        migrations.RenameField(
            model_name='class',
            old_name='ClassName',
            new_name='className',
        ),
        migrations.AlterField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(related_name='students', to='main.UserProfile'),
        ),
    ]
