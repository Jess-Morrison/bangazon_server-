# Generated by Django 4.1.5 on 2023-01-28 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bangazonapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproducts',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bangazonapi.user'),
            preserve_default=False,
        ),
    ]
