from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_de', 'title_ta', 'github_url']
    search_fields = ['title_en', 'title_de', 'title_ta', 'description_en', 'company_name_en', 'company_name_de', 'company_name_ta']
    fieldsets = (
        ('Basic Info', {
            'fields': ('github_url', 'demo_url', 'date_from', 'date_to', 'show_month_year_only', 'profiles')
        }),
        ('English', {
            'fields': ('title_en', 'description_en', 'tech_stack_en', 'company_name_en', 'company_linkedin_url_en')
        }),
        ('German', {
            'fields': ('title_de', 'description_de', 'tech_stack_de', 'company_name_de', 'company_linkedin_url_de'),
            'classes': ('collapse',)
        }),
        ('Tamil', {
            'fields': ('title_ta', 'description_ta', 'tech_stack_ta', 'company_name_ta', 'company_linkedin_url_ta'),
            'classes': ('collapse',)
        }),
    )
    filter_horizontal = ['profiles']
