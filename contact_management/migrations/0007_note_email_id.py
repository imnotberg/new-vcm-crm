# Generated by Django 3.1.5 on 2021-02-04 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_management', '0006_auto_20210203_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='email_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]