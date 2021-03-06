# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 15:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, null=True, unique=True, verbose_name='email address')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('name', models.CharField(max_length=32)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=64, verbose_name='主机')),
                ('ip_addr', models.GenericIPAddressField(unique=True, verbose_name='IP地址')),
                ('port', models.PositiveIntegerField(default=22, verbose_name='端口号')),
                ('enable', models.BooleanField(default=True, verbose_name='当前状态')),
            ],
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='主机组')),
            ],
        ),
        migrations.CreateModel(
            name='HostToUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audit.Host')),
            ],
        ),
        migrations.CreateModel(
            name='HostUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth_type', models.SmallIntegerField(choices=[(0, '密码验证'), (1, '密钥验证')], default=0)),
                ('username', models.CharField(max_length=64, verbose_name='用户名')),
                ('password', models.CharField(max_length=128, verbose_name='密码')),
            ],
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='数据中心')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='hostuser',
            unique_together=set([('auth_type', 'username', 'password')]),
        ),
        migrations.AddField(
            model_name='hosttouser',
            name='host_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audit.HostUser'),
        ),
        migrations.AddField(
            model_name='hostgroup',
            name='host_2_user',
            field=models.ManyToManyField(blank=True, to='audit.HostToUser'),
        ),
        migrations.AddField(
            model_name='host',
            name='IDC',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audit.IDC', verbose_name='数据中心'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='host_2_user',
            field=models.ManyToManyField(blank=True, to='audit.HostToUser'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='host_groups',
            field=models.ManyToManyField(blank=True, to='audit.HostGroup'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='hosttouser',
            unique_together=set([('host', 'host_user')]),
        ),
    ]
