# Generated by Django 2.2.2 on 2022-07-13 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0004_auto_20220713_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanrecord',
            name='count',
            field=models.IntegerField(default=0, verbose_name='贷款次数'),
        ),
        migrations.AlterField(
            model_name='loanrecord',
            name='content',
            field=models.IntegerField(default=0, verbose_name='借贷描述'),
        ),
        migrations.AlterField(
            model_name='loanrecord',
            name='status',
            field=models.IntegerField(default=0, verbose_name='状态(0待审核/ 1审核中/   2审核通过/  3不通过/   4取消)'),
        ),
    ]
