# Generated by Django 4.2.3 on 2023-07-17 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0002_tag_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='view_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]