# Generated by Django 3.2.4 on 2022-04-23 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20220419_0637'),
        ('jobs', '0004_auto_20220422_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='applicants',
            field=models.ManyToManyField(blank=True, to='account.Profile'),
        ),
    ]
