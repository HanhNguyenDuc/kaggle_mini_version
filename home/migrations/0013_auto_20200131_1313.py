# Generated by Django 3.0.2 on 2020-01-31 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_auto_20200131_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='id',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
