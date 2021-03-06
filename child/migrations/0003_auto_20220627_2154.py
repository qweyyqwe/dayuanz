# Generated by Django 2.2.2 on 2022-06-27 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('child', '0002_auto_20220627_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birth',
            field=models.DateTimeField(blank=True, null=True, verbose_name='出生日期'),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.SmallIntegerField(choices=[(0, 'nan'), (1, 'nv')], null=True, verbose_name='性别'),
        ),
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='昵称'),
        ),
    ]
