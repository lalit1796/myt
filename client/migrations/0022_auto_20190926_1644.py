# Generated by Django 2.2.2 on 2019-09-26 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0021_auto_20190926_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='adult_per_cost',
            field=models.IntegerField(blank=True, default=0, help_text='Cost per adult', null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='kids_per_cost',
            field=models.IntegerField(blank=True, default=0, help_text='Cost per Kids', null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='adult_bill',
            field=models.IntegerField(blank=True, default=0, help_text='Net bill for adults', null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='kids_bill',
            field=models.IntegerField(blank=True, default=0, help_text='Net bill for kids', null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_count',
            field=models.IntegerField(blank=True, default=0, help_text='Number of Individuals', null=True),
        ),
    ]