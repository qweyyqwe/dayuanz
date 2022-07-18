# Generated by Django 2.2.2 on 2022-07-15 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0008_auto_20220715_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='topuprecord',
            name='code',
            field=models.CharField(default='', max_length=30, verbose_name='生成唯一code'),
        ),
        migrations.AddField(
            model_name='topuprecord',
            name='serial_number',
            field=models.CharField(default='', max_length=50, verbose_name='订单流水号'),
        ),
    ]
