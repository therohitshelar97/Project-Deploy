# Generated by Django 5.0 on 2024-01-04 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petApp', '0010_alter_address_animals_alter_address_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='cname',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
