# Generated by Django 2.2.7 on 2022-06-20 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='code',
            field=models.CharField(max_length=255, null=True, unique=True, verbose_name='邀请码'),
        ),
    ]
