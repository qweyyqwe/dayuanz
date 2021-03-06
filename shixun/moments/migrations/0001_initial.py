# Generated by Django 2.2.7 on 2022-06-26 09:09

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PypMoments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000, verbose_name='朋友圈内容')),
                ('create_time', models.DateTimeField(default=datetime.datetime(2022, 6, 26, 9, 9, 8, 837754, tzinfo=utc), verbose_name='发布时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户id')),
            ],
            options={
                'verbose_name_plural': '朋友圈',
                'db_table': 'pyp_moments',
            },
        ),
        migrations.CreateModel(
            name='PypPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(default='', max_length=256, verbose_name='图片地址')),
                ('create_time', models.DateTimeField(default=datetime.datetime(2022, 6, 26, 9, 9, 8, 837754, tzinfo=utc), verbose_name='发布时间')),
                ('moments', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moments.PypMoments', verbose_name='朋友圈')),
            ],
            options={
                'verbose_name_plural': '朋友圈图片',
                'db_table': 'pyp_picture',
            },
        ),
        migrations.CreateModel(
            name='PypComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200, verbose_name='评论内容')),
                ('create_time', models.DateTimeField(default=datetime.datetime(2022, 6, 26, 9, 9, 8, 837754, tzinfo=utc), verbose_name='发布时间')),
                ('pid', models.IntegerField(default=0, verbose_name='评论的id')),
                ('moments', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moments.PypMoments', verbose_name='朋友圈')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户id')),
            ],
            options={
                'verbose_name_plural': '朋友圈评论',
                'db_table': 'pyp_comment',
            },
        ),
    ]
