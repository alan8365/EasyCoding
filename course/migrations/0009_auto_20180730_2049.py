# Generated by Django 2.0.7 on 2018-07-30 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_content_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='code',
            field=models.TextField(default='', max_length=3000),
        ),
    ]
