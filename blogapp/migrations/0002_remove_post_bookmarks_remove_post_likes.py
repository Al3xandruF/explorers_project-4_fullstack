# Generated by Django 4.2.3 on 2023-08-14 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='bookmarks',
        ),
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]
