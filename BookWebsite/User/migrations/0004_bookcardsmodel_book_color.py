# Generated by Django 4.2.1 on 2023-05-18 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_bookcardsmodel_book_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookcardsmodel',
            name='book_color',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
