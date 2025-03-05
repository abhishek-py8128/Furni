# Generated by Django 5.0.4 on 2024-06-26 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0012_alter_orderdetail_product_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='paymentProcess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('amount', models.CharField(max_length=100)),
                ('payment_id', models.CharField(max_length=100)),
                ('paid', models.BooleanField(default=False)),
            ],
        ),
    ]
