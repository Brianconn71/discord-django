# Generated by Django 3.2.4 on 2021-11-26 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20211126_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
