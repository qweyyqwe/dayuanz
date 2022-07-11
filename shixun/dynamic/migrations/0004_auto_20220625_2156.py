# Generated by Django 2.2.7 on 2022-06-25 13:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic', '0003_auto_20220625_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='dynamic',
            name='ic_people',
            field=models.CharField(default=1, max_length=50, verbose_name='审核员'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dynamic',
            name='publish_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 13, 56, 57, 528743, tzinfo=utc), verbose_name='发布时间'),
        ),
    ]
