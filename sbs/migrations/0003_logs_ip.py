# Generated by Django 2.2.6 on 2020-08-18 16:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('sbs', '0002_logs'),
    ]

    operations = [
        migrations.AddField(
            model_name='logs',
            name='ip',
            field=models.CharField(max_length=20, null=True),
        ),
    ]