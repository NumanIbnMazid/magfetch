# Generated by Django 2.1.7 on 2019-04-24 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contribution', '0003_comment_is_special'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='is_special',
            field=models.BooleanField(default=False, verbose_name='is_special'),
        ),
    ]