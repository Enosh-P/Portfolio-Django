from django.db import models
from profiles.models import Profile

class Project(models.Model):
    # Language-specific fields
    title_en = models.CharField(max_length=100)
    title_de = models.CharField(max_length=100, blank=True)
    title_ta = models.CharField(max_length=100, blank=True)
    
    description_en = models.TextField()
    description_de = models.TextField(blank=True)
    description_ta = models.TextField(blank=True)
    
    tech_stack_en = models.CharField(max_length=200)
    tech_stack_de = models.CharField(max_length=200, blank=True)
    tech_stack_ta = models.CharField(max_length=200, blank=True)
    
    github_url = models.URLField(blank=True)
    profiles = models.ManyToManyField(Profile)

    def __str__(self):
        return self.title_en
    
    def get_title(self, language='en'):
        """Get title in specified language"""
        field_name = f'title_{language}'
        title = getattr(self, field_name, None)
        return title or self.title_en
    
    def get_description(self, language='en'):
        """Get description in specified language"""
        field_name = f'description_{language}'
        desc = getattr(self, field_name, None)
        return desc or self.description_en
    
    def get_tech_stack(self, language='en'):
        """Get tech stack in specified language"""
        field_name = f'tech_stack_{language}'
        tech = getattr(self, field_name, None)
        return tech or self.tech_stack_en
