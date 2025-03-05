# Generated by Django 5.0.4 on 2024-06-18 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_cart_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(default=True)),
                ('product_name', models.CharField(max_length=15)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('qty', models.PositiveIntegerField(default=1)),
                ('price', models.IntegerField()),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Accepted', 'Accepted'), ('Packed', 'Packed'), ('On the Way', 'On the Way'), ('Delivered', 'Delivered'), ('Cancel', 'Cancel')], default='Pending', max_length=50)),
            ],
        ),
    ]
