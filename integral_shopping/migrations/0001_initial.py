# Generated by Django 2.2.2 on 2022-06-29 02:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PointsMall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True, verbose_name='商品名字')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='简介')),
                ('image', models.CharField(blank=True, max_length=168, null=True, verbose_name='简介图片')),
                ('price', models.IntegerField(default=0, verbose_name='价格')),
                ('count', models.IntegerField(default=0, verbose_name='库存')),
                ('lock_count', models.IntegerField(default=0, verbose_name='锁定库存')),
                ('sale_count', models.IntegerField(default=0, verbose_name='销量')),
            ],
            options={
                'db_table': 'integral_shopping_pointsmall',
            },
        ),
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=168, verbose_name='url地址')),
                ('pointsmallid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='integral_shopping.PointsMall', verbose_name='积分商城图片')),
            ],
            options={
                'db_table': 'integral_shopping_img',
            },
        ),
    ]