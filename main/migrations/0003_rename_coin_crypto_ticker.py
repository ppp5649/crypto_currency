# Generated by Django 4.0.2 on 2022-06-02 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_crypto_delete_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crypto',
            old_name='coin',
            new_name='ticker',
        ),
    ]
