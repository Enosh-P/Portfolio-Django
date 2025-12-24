# Generated manually - migrate data and remove old fields

from django.db import migrations


def migrate_project_data(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')
    for project in Project.objects.all():
        # Copy existing data to _en fields
        # Check if old fields exist (they will be removed in this migration)
        if hasattr(project, 'title') and project.title and not project.title_en:
            project.title_en = project.title
        if hasattr(project, 'description') and project.description and not project.description_en:
            project.description_en = project.description
        if hasattr(project, 'tech_stack') and project.tech_stack and not project.tech_stack_en:
            project.tech_stack_en = project.tech_stack
        project.save()


def reverse_migrate_project_data(apps, schema_editor):
    # Reverse migration - copy _en fields back to old fields
    Project = apps.get_model('projects', 'Project')
    for project in Project.objects.all():
        if hasattr(project, 'title'):
            project.title = project.title_en
        if hasattr(project, 'description'):
            project.description = project.description_en
        if hasattr(project, 'tech_stack'):
            project.tech_stack = project.tech_stack_en
        project.save()


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_add_multilingual_fields'),
    ]

    operations = [
        migrations.RunPython(migrate_project_data, reverse_migrate_project_data),
        # Remove old fields
        migrations.RemoveField(
            model_name='project',
            name='title',
        ),
        migrations.RemoveField(
            model_name='project',
            name='description',
        ),
        migrations.RemoveField(
            model_name='project',
            name='tech_stack',
        ),
    ]


