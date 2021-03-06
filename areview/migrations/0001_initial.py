# Generated by Django 2.1.2 on 2018-11-09 02:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_number', models.IntegerField(db_index=True)),
                ('review_text', models.CharField(db_index=True, max_length=500)),
                ('pub_date', models.DateTimeField(db_index=True, verbose_name='date published')),
                ('review_header', models.CharField(db_index=True, max_length=200)),
                ('review_rating', models.CharField(db_index=True, max_length=200)),
                ('review_author', models.CharField(db_index=True, max_length=200)),
                ('asin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='areview.Asin')),
            ],
        ),
    ]
