# Generated by Django 2.0.2 on 2018-03-12 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='host',
            old_name='is_virtaul',
            new_name='is_virtual',
        ),
        migrations.RenameField(
            model_name='host',
            old_name='salt_status',
            new_name='minion_status',
        ),
    ]
