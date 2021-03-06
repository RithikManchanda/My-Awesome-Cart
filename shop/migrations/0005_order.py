# Generated by Django 2.2.2 on 2019-07-04 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20190628_2137'),
    ]

    operations = [
        migrations.CreateModel(
            name='order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('items_json', models.CharField(max_length=5000)),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(default='', max_length=50)),
                ('phone', models.CharField(default='', max_length=50)),
                ('city', models.CharField(default='', max_length=50)),
                ('state', models.CharField(default='', max_length=50)),
                ('pin_code', models.CharField(default='', max_length=50)),
                ('address', models.CharField(default='', max_length=50)),
            ],
        ),
    ]
