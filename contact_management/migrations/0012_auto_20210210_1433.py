# Generated by Django 3.1.5 on 2021-02-10 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_management', '0011_auto_20210210_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emaildatafull',
            name='data',
            field=models.JSONField(),
        ),
    ]
