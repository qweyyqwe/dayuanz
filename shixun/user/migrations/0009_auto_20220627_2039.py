# Generated by Django 2.2.7 on 2022-06-27 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_userinformation'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='userinformation',
            table='user_information',
        ),
    ]