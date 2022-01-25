# Generated by Django 3.2.4 on 2022-01-25 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('firstname', models.CharField(max_length=150)),
                ('lastname', models.CharField(max_length=150)),
                ('company_name', models.CharField(max_length=150)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('verified', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('Company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='companies.companyaccount')),
                ('logo', models.BinaryField(editable=True, null=True)),
                ('content_type', models.CharField(help_text='The MIMEType of the file', max_length=256, null=True)),
                ('size_of_company', models.CharField(choices=[('SB', 'Small Business'), ('ME', 'Mid Market enterprise'), ('EN', 'Enterprise')], max_length=25)),
                ('company_industries', models.CharField(choices=[('T', 'Tech'), ('ARCH', 'Architecture'), ('TR', 'Translation'), ('DES', 'Design'), ('MA', 'Media and Advertising'), ('ME', 'Medicine')], max_length=25)),
                ('company_type', models.CharField(choices=[('PRV', 'Private company'), ('PUB', 'Public Company'), ('NPO', 'Non Profit Organization')], max_length=25)),
                ('no_of_employees', models.CharField(max_length=9)),
                ('isInternational', models.BooleanField()),
                ('headquarters', models.CharField(max_length=30)),
                ('founded_at', models.DateTimeField()),
            ],
        ),
    ]
