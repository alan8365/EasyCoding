# Generated by Django 2.0.7 on 2018-10-09 00:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0014_remove_fill_fill_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='fill_answer',
            name='fill',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='course.Fill'),
        ),
    ]