# Generated by Django 2.2.2 on 2022-07-13 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0005_auto_20220713_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanrecord',
            name='code',
            field=models.CharField(default='', max_length=30, verbose_name='唯一标识'),
        ),
        migrations.AlterField(
            model_name='loanrecord',
            name='loan_money',
            field=models.IntegerField(verbose_name='贷款金额'),
        ),
    ]
