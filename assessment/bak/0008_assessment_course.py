# Generated by Django 2.0.7 on 2018-08-02 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0009_auto_20180730_2049'),
        ('assessment', '0007_delete_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='course.Course'),
        ),
    ]
