# Generated by Django 5.0 on 2024-01-11 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petApp', '0014_order_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.FloatField(null=True),
        ),
    ]
