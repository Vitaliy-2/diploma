# Generated by Django 5.1.2 on 2024-10-30 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('STOservice', '0002_employee_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('comment', models.TextField(verbose_name='Комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('status', models.IntegerField(choices=[(0, 'Не проверен'), (1, 'Проверен')], default=0, verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ['-created_at'],
            },
        ),
    ]
