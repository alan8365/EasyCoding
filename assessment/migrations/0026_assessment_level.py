# Generated by Django 2.0.7 on 2018-10-08 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0025_auto_20180911_0533'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='level',
            field=models.SmallIntegerField(default=1),
        ),
    ]
