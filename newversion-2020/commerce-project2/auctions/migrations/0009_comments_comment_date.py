# Generated by Django 3.0.8 on 2020-07-11 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_comments_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='comment_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]