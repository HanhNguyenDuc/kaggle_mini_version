# Generated by Django 3.0.2 on 2020-03-11 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20200201_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='data_test',
            field=models.CharField(default='/', max_length=100),
        ),
    ]