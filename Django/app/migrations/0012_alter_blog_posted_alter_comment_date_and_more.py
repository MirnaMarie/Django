# Generated by Django 5.0.6 on 2024-06-25 17:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_blog_posted_alter_comment_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2024, 6, 25, 20, 12, 5, 544357), verbose_name='Опубликована'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2024, 6, 25, 20, 12, 5, 545354), verbose_name='Дата комментария'),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2024, 6, 25, 20, 12, 5, 545354), verbose_name='Дата покупки'),
        ),
        migrations.AlterField(
            model_name='visits',
            name='date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2024, 6, 25, 20, 12, 5, 546351), verbose_name='Дата посещения'),
        ),
    ]