from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0004_project_company_linkedin_url_de_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="show_month_year_only",
            field=models.BooleanField(default=False),
        ),
    ]
