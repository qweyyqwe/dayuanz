# Generated by Django 2.2.2 on 2022-06-26 03:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discuss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField()),
                ('discuss_fatherid', models.IntegerField(blank=True, null=True)),
                ('plazaid', models.IntegerField()),
                ('content', models.CharField(max_length=268, verbose_name='评论内容')),
                ('discuss_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='评论时间')),
                ('starts', models.IntegerField(verbose_name='0显示/ 1删除')),
            ],
            options={
                'db_table': 'plaza_discuss',
            },
        ),
        migrations.CreateModel(
            name='Plaza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.IntegerField(verbose_name='发布人id')),
                ('title', models.CharField(blank=True, max_length=268, null=True, verbose_name='标题')),
                ('content', models.CharField(max_length=268, verbose_name='内容')),
                ('code', models.CharField(blank=True, max_length=50, null=True, verbose_name='唯一标识')),
                ('begin_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='发布时间')),
                ('over_time', models.DateTimeField(blank=True, null=True, verbose_name='删除时间')),
                ('start', models.IntegerField(default=0, verbose_name='0显示/  1删除动态')),
                ('checkid', models.IntegerField(blank=True, null=True, verbose_name='审核人id')),
                ('check_start', models.IntegerField(default=0, verbose_name='0未审核    /1审核中   /2通过    /3失败')),
                ('check_content', models.CharField(blank=True, max_length=268, null=True)),
            ],
            options={
                'db_table': 'plaza_plazas',
            },
        ),
    ]