# Generated by Django 2.0.7 on 2018-07-30 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_content_istitle'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='charpter',
            new_name='chapter',
        ),
    ]