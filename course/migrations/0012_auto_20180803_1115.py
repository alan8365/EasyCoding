# Generated by Django 2.0.7 on 2018-08-03 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0011_remove_content_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='content',
            field=models.TextField(max_length=2100),
        ),
    ]
