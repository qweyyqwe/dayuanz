# Generated by Django 2.2.2 on 2022-06-29 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integral_shopping', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointsmall',
            name='status',
            field=models.IntegerField(default=0, verbose_name='状态0存在/   1下架'),
        ),
    ]