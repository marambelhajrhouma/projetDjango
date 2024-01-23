# Generated by Django 5.0.1 on 2024-01-19 19:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_id', models.AutoField(primary_key=True, serialize=False)),
                ('department_name', models.CharField(choices=[('Administration', 'Administration'), ('Information Technology', 'Information Technology (IT)'), ('Human Resources', 'Human Resources (HR)'), ('Finance', 'Finance')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('position_id', models.AutoField(primary_key=True, serialize=False)),
                ('position_name', models.CharField(choices=[('admin', 'Admin'), ('RH', 'RH'), ('regular_employee', 'Regular Employee')], default='regular_employee', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('employee_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='employee.department')),
                ('groups', models.ManyToManyField(blank=True, related_name='employee_groups', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='employee_permissions', to='auth.permission')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='employee.position')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
