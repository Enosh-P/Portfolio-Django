from django.db import models

class SkillCategory(models.Model):
    """Category for grouping skills (C++ Developer, Python Developer, ML Engineer, CI/CD Skills)"""
    slug = models.SlugField(unique=True, max_length=50)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon identifier for the category")
    
    # Language-specific names
    name_en = models.CharField(max_length=100)
    name_de = models.CharField(max_length=100, blank=True)
    name_ta = models.CharField(max_length=100, blank=True)
    
    order = models.IntegerField(default=0, help_text="Display order")
    
    class Meta:
        verbose_name_plural = "Skill Categories"
        ordering = ['order', 'slug']
    
    def __str__(self):
        return self.name_en
    
    def get_name(self, language='en'):
        """Get name in specified language"""
        field_name = f'name_{language}'
        name = getattr(self, field_name, None)
        return name or self.name_en


class Skill(models.Model):
    """Individual skill within a category"""
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    order = models.IntegerField(default=0, help_text="Display order within category")
    
    # Language-specific fields
    name_en = models.CharField(max_length=200)
    name_de = models.CharField(max_length=200, blank=True)
    name_ta = models.CharField(max_length=200, blank=True)
    
    description_en = models.TextField(blank=True)
    description_de = models.TextField(blank=True)
    description_ta = models.TextField(blank=True)
    
    class Meta:
        ordering = ['category', 'order', 'name_en']
    
    def __str__(self):
        return f"{self.category.name_en}: {self.name_en}"
    
    def get_name(self, language='en'):
        """Get name in specified language"""
        field_name = f'name_{language}'
        name = getattr(self, field_name, None)
        return name or self.name_en
    
    def get_description(self, language='en'):
        """Get description in specified language"""
        field_name = f'description_{language}'
        desc = getattr(self, field_name, None)
        return desc or self.description_en
