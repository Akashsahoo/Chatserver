# Generated by Django 2.2.15 on 2022-08-21 00:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_auto_20220820_2130'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='is_active',
            new_name='read',
        ),
    ]
