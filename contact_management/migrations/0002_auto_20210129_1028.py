# Generated by Django 3.1.5 on 2021-01-29 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='tags',
            field=models.ManyToManyField(related_name='account_tags', to='contact_management.Tag'),
        ),
        migrations.AddField(
            model_name='lead',
            name='tags',
            field=models.ManyToManyField(related_name='lead_tags', to='contact_management.Tag'),
        ),
    ]
