# Generated by Django 5.0.2 on 2024-02-20 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petApp', '0018_delete_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_date',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
