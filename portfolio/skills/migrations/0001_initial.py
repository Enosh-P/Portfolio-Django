# Generated manually for skills app

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SkillCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=50, unique=True)),
                ('icon', models.CharField(blank=True, help_text='Icon identifier for the category', max_length=50)),
                ('name_en', models.CharField(max_length=100)),
                ('name_de', models.CharField(blank=True, max_length=100)),
                ('name_ta', models.CharField(blank=True, max_length=100)),
                ('order', models.IntegerField(default=0, help_text='Display order')),
            ],
            options={
                'verbose_name_plural': 'Skill Categories',
                'ordering': ['order', 'slug'],
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0, help_text='Display order within category')),
                ('name_en', models.CharField(max_length=200)),
                ('name_de', models.CharField(blank=True, max_length=200)),
                ('name_ta', models.CharField(blank=True, max_length=200)),
                ('description_en', models.TextField(blank=True)),
                ('description_de', models.TextField(blank=True)),
                ('description_ta', models.TextField(blank=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='skills.skillcategory')),
            ],
            options={
                'ordering': ['category', 'order', 'name_en'],
            },
        ),
    ]


