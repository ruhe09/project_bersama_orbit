# Generated by Django 3.2.8 on 2022-05-29 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buset', '0004_auto_20220529_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='posting',
            name='post_date_modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='posting',
            name='post_slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
