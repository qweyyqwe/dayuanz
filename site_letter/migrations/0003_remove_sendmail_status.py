# Generated by Django 2.2.2 on 2022-07-11 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_letter', '0002_auto_20220711_1940'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sendmail',
            name='status',
        ),
    ]
