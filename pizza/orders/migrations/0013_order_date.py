# Generated by Django 3.0.7 on 2020-08-09 05:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_remove_order_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]