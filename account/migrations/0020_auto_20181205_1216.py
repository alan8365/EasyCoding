# Generated by Django 2.0.7 on 2018-12-05 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_auto_20181205_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement_get',
            name='achievement',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Achievement'),
        ),
    ]
