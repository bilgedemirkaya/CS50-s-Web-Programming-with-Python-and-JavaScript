# Generated by Django 3.0.8 on 2020-07-13 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_auto_20200712_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='category',
            field=models.CharField(blank=True, choices=[('Home', 'Home'), ('Outdoor', 'Outdoor'), ('Fashion', 'Fashion'), ('Heath', 'Health'), ('Toys', 'Toys'), ('Books', 'Books')], max_length=32),
        ),
    ]
