# Generated by Django 5.0 on 2023-12-23 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('petApp', '0003_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='cid',
        ),
    ]
