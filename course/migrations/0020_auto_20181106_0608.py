# Generated by Django 2.0.7 on 2018-11-06 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0019_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Lesson'),
        ),
    ]