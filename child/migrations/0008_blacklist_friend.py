# Generated by Django 2.2.2 on 2022-07-08 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('child', '0007_auto_20220708_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='blacklist',
            name='friend',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='child.Friends', verbose_name='朋友id'),
        ),
    ]