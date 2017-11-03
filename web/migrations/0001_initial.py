# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-11-02 07:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('nid', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128, verbose_name='\u6587\u7ae0\u6807\u9898')),
                ('summary', models.CharField(max_length=255, verbose_name='\u6587\u7ae0\u7b80\u4ecb')),
                ('read_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('up_count', models.IntegerField(default=0)),
                ('down_count', models.IntegerField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('article_type', models.IntegerField(choices=[(1, 'Python'), (2, 'Linux'), (3, 'OpenStack'), (4, 'GoLang')], default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Article2Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Article', verbose_name='\u6587\u7ae0')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='\u6587\u7ae0\u5185\u5bb9')),
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='web.Article', verbose_name='\u6240\u5c5e\u6587\u7ae0')),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('nid', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64, verbose_name='\u4e2a\u4eba\u535a\u5ba2\u6807\u9898')),
                ('site', models.CharField(max_length=32, unique=True, verbose_name='\u4e2a\u4eba\u535a\u5ba2\u524d\u7f00')),
                ('theme', models.CharField(max_length=32, verbose_name='\u535a\u5ba2\u4e3b\u9898')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='\u5206\u7c7b\u6807\u9898')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Blog', verbose_name='\u6240\u5c5e\u535a\u5ba2')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('nid', models.BigAutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=255, verbose_name='\u8bc4\u8bba\u5185\u5bb9')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Article', verbose_name='\u8bc4\u8bba\u6587\u7ae0')),
                ('reply', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='back', to='web.Comment', verbose_name='\u56de\u590d\u8bc4\u8bba')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='\u6807\u7b7e\u540d\u79f0')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Blog', verbose_name='\u6240\u5c5e\u535a\u5ba2')),
            ],
        ),
        migrations.CreateModel(
            name='UpDown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('up', models.BooleanField(verbose_name='\u662f\u5426\u8d5e')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Article', verbose_name='\u6587\u7ae0')),
            ],
        ),
        migrations.CreateModel(
            name='UserFans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('nid', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=32, unique=True)),
                ('password', models.CharField(max_length=32)),
                ('nickname', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('img', models.ImageField(upload_to=b'')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('fans', models.ManyToManyField(through='web.UserFans', to='web.UserInfo')),
            ],
        ),
        migrations.AddField(
            model_name='userfans',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='web.UserInfo', verbose_name='\u7c89\u4e1d'),
        ),
        migrations.AddField(
            model_name='userfans',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='web.UserInfo', verbose_name='\u535a\u4e3b'),
        ),
        migrations.AddField(
            model_name='updown',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.UserInfo', verbose_name='\u8d5e\u6216\u8e29\u7528\u6237'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.UserInfo', verbose_name='\u8bc4\u8bba\u8005'),
        ),
        migrations.AddField(
            model_name='blog',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='web.UserInfo'),
        ),
        migrations.AddField(
            model_name='article2tag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Tag', verbose_name='\u6807\u7b7e'),
        ),
        migrations.AddField(
            model_name='article',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Blog', verbose_name='\u6240\u5c5e\u535a\u5ba2'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Category', verbose_name='\u6587\u7ae0\u7c7b\u578b'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(through='web.Article2Tag', to='web.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='userfans',
            unique_together=set([('user', 'follower')]),
        ),
        migrations.AlterUniqueTogether(
            name='updown',
            unique_together=set([('article', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='article2tag',
            unique_together=set([('article', 'tag')]),
        ),
    ]