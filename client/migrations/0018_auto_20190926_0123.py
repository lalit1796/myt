# Generated by Django 2.2.2 on 2019-09-25 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0017_order_service_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product_uid',
            field=models.CharField(default=0, help_text='Product UID', max_length=200),
        ),
    ]
