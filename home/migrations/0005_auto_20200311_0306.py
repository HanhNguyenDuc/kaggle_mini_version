# Generated by Django 3.0.2 on 2020-03-11 03:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_contest_data_test'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contest',
            old_name='data_test',
            new_name='test_data_path',
        ),
    ]
