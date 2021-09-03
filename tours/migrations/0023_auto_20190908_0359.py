# Generated by Django 2.2.2 on 2019-09-07 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0022_auto_20190906_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='itinerary',
            field=models.ForeignKey(help_text='Select or Create Itinerary.', on_delete=django.db.models.deletion.PROTECT, related_name='itinerary', to='props.Itinerary'),
        ),
    ]