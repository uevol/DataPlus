# Generated by Django 2.0.2 on 2018-03-05 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0002_auto_20180305_0947'),
    ]

    operations = [
        migrations.AddField(
            model_name='perm',
            name='menu',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='admins.Menu'),
            preserve_default=False,
        ),
    ]
