from django.db import migrations, models


def _get_existing_columns(schema_editor, table_name):
    with schema_editor.connection.cursor() as cursor:
        return {
            column.name
            for column in schema_editor.connection.introspection.get_table_description(cursor, table_name)
        }


def add_cv_file_if_missing(apps, schema_editor):
    Profile = apps.get_model('profiles', 'Profile')
    table_name = Profile._meta.db_table
    existing_columns = _get_existing_columns(schema_editor, table_name)

    if 'cv_file' in existing_columns:
        return

    field = models.FileField(blank=True, null=True, upload_to='cv/')
    field.set_attributes_from_name('cv_file')
    schema_editor.add_field(Profile, field)

def remove_cv_file_if_present(apps, schema_editor):
    Profile = apps.get_model('profiles', 'Profile')
    table_name = Profile._meta.db_table
    existing_columns = _get_existing_columns(schema_editor, table_name)

    if 'cv_file' not in existing_columns:
        return

    field = models.FileField(blank=True, null=True, upload_to='cv/')
    field.set_attributes_from_name('cv_file')
    schema_editor.remove_field(Profile, field)


def add_missing_multilingual_cv_columns(apps, schema_editor):
    Profile = apps.get_model('profiles', 'Profile')
    table_name = Profile._meta.db_table
    existing_columns = _get_existing_columns(schema_editor, table_name)

    for field_name in ('cv_file_en', 'cv_file_de', 'cv_file_ta'):
        if field_name in existing_columns:
            continue
        field = models.FileField(blank=True, null=True, upload_to='cv/')
        field.set_attributes_from_name(field_name)
        schema_editor.add_field(Profile, field)


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_remove_category_skill_category_category_skills'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(add_cv_file_if_missing, remove_cv_file_if_present),
                migrations.RunPython(add_missing_multilingual_cv_columns, migrations.RunPython.noop),
            ],
            state_operations=[
                migrations.AddField(
                    model_name='profile',
                    name='cv_file',
                    field=models.FileField(blank=True, null=True, upload_to='cv/'),
                ),
            ],
        ),
    ]
