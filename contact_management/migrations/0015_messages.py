# Generated by Django 3.1.5 on 2021-02-10 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_management', '0014_delete_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
