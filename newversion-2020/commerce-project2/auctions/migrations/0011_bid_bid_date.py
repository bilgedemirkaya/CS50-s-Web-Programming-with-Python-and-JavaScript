# Generated by Django 3.0.8 on 2020-07-12 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='bid_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]