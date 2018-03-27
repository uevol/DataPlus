# Generated by Django 2.0.2 on 2018-03-26 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('file_type', models.CharField(default='other', max_length=100)),
                ('created_by', models.CharField(blank=True, max_length=80, null=True)),
                ('comment', models.CharField(blank=True, max_length=200, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'upload_file',
            },
        ),
    ]
