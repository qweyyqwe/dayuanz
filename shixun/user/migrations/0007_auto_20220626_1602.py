# Generated by Django 2.2.7 on 2022-06-26 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_usergroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30, verbose_name='名称')),
                ('url', models.CharField(default='', max_length=256, verbose_name='角色资源地址')),
                ('status', models.IntegerField(default=1, verbose_name='角色资源状态')),
                ('pid', models.IntegerField(verbose_name='父类id')),
            ],
            options={
                'db_table': 'resource',
            },
        ),
        migrations.AlterField(
            model_name='usergroup',
            name='name',
            field=models.CharField(default='', max_length=30, verbose_name='名称'),
        ),
        migrations.AddField(
            model_name='usergroup',
            name='resource',
            field=models.ManyToManyField(to='user.Resource'),
        ),
    ]
