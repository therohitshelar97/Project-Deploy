# Generated by Django 5.0.2 on 2024-03-07 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petApp', '0021_order_history_alternate_phone_order_history_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_history',
            name='order_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]