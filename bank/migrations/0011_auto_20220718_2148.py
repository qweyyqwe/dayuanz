# Generated by Django 2.2.2 on 2022-07-18 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0010_auto_20220718_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanrecord',
            name='have_money',
            field=models.IntegerField(default=0, verbose_name='已投资金额'),
        ),
    ]
