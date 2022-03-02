# Generated by Django 3.1.1 on 2022-03-02 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account_type',
            field=models.CharField(choices=[('0', 'Administrator'), ('1', 'Merchant')], default='1', max_length=50),
        ),
    ]
