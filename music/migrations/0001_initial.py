# Generated by Django 2.0.5 on 2018-05-30 15:26

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('info', tinymce.models.HTMLField(null=True)),
                ('image', models.ImageField(default='media/album_image/default.jpg', null=True, upload_to='media/album_image/')),
                ('auth', models.CharField(blank=True, max_length=40, null=True)),
                ('isDelete', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserInfo')),
            ],
        ),
        migrations.CreateModel(
            name='CollDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('isDelete', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserInfo')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default='2018-05-30 15:03:10')),
                ('content', models.CharField(max_length=140)),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('info', tinymce.models.HTMLField(null=True)),
                ('src', models.FileField(upload_to='static/media/music/')),
                ('click', models.IntegerField(default=0)),
                ('tuijian', models.IntegerField(default=0)),
                ('isDelete', models.BooleanField(default=False)),
                ('album', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='music.Album')),
            ],
        ),
        migrations.CreateModel(
            name='PlayList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('music', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Music')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserInfo')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('pid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='music.Type')),
            ],
        ),
        migrations.AddField(
            model_name='history',
            name='music',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Music'),
        ),
        migrations.AddField(
            model_name='history',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserInfo'),
        ),
        migrations.AddField(
            model_name='comment',
            name='music',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='music.Music'),
        ),
        migrations.AddField(
            model_name='comment',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserInfo'),
        ),
        migrations.AddField(
            model_name='comment',
            name='pcom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='music.Comment'),
        ),
        migrations.AddField(
            model_name='colldetail',
            name='coll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Collection'),
        ),
        migrations.AddField(
            model_name='colldetail',
            name='music',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Music'),
        ),
        migrations.AddField(
            model_name='album',
            name='typed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Type'),
        ),
    ]
