# Generated by Django 4.1.2 on 2022-11-15 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0004_alter_teacher_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='role',
            field=models.CharField(choices=[('teacher', 'TEACHER')], default='TEACHER', max_length=10),
        ),
    ]
