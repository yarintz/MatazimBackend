# Generated by Django 3.2.8 on 2022-04-26 15:17

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_auto_20220426_1758'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PlanName', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='UserClasses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ClassName', models.CharField(max_length=32)),
                ('NumberOfStudents', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)])),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SchoolName', models.CharField(max_length=32)),
                ('Plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan', to='main.plan')),
            ],
        ),
        migrations.AddField(
            model_name='class',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='school', to='main.school'),
            preserve_default=False,
        ),
    ]
