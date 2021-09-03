# Generated by Django 2.2.2 on 2019-09-18 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0023_auto_20190908_0359'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='make_exclusive',
            field=models.BooleanField(default=0, help_text='For exclusive packages.'),
        ),
        migrations.AddField(
            model_name='package',
            name='make_inbudget',
            field=models.BooleanField(default=0, help_text='For budget packages.'),
        ),
        migrations.AddField(
            model_name='package',
            name='make_indemand',
            field=models.BooleanField(default=0, help_text='For in demand packages.'),
        ),
        migrations.AddField(
            model_name='package',
            name='make_limitedoffer',
            field=models.BooleanField(default=0, help_text='For limited packages.'),
        ),
    ]