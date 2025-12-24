# Generated manually for multilingual support

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        # Add new language-specific fields
        migrations.AddField(
            model_name='project',
            name='title_en',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='title_de',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='project',
            name='title_ta',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='project',
            name='description_en',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='description_de',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='description_ta',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='tech_stack_en',
            field=models.CharField(max_length=200, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='tech_stack_de',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='project',
            name='tech_stack_ta',
            field=models.CharField(blank=True, max_length=200),
        ),
        # Data migration will be in next migration
    ]


