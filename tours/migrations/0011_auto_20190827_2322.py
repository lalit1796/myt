# Generated by Django 2.2.2 on 2019-08-27 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0010_auto_20190827_2317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='city',
        ),
        migrations.AddField(
            model_name='package',
            name='tags',
            field=models.TextField(default=0, help_text='Eg: Goa beach, Snow, Holiday in Manali'),
        ),
    ]
