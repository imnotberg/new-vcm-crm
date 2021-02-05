# Generated by Django 3.1.5 on 2021-02-04 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contact_management', '0007_note_email_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='total',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoice_for_order_item', to='contact_management.invoice'),
        ),
    ]
