# Generated by Django 4.2.1 on 2023-05-18 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0005_bookcardsmodel_book_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookcardsmodel',
            name='shop_cost',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]