# Generated by Django 3.2.6 on 2021-08-24 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid19BotApp', '0003_covid7dayinfo_new_cases'),
    ]

    operations = [
        migrations.AddField(
            model_name='covid7dayinfo',
            name='Chinese_name',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='covid7dayinfo',
            name='date_str',
            field=models.IntegerField(null=True),
        ),
    ]
