# Generated by Django 2.1.7 on 2019-02-20 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0002_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='subject',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='subject'),
        ),
    ]
