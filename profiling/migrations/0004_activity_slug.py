# Generated by Django 2.2.2 on 2019-09-10 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiling', '0003_auto_20190823_0352'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='slug',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]