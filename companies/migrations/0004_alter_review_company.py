# Generated by Django 3.2.4 on 2022-04-07 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_alter_review_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='company',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='companies.companyprofile'),
        ),
    ]
