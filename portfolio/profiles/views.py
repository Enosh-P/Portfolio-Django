from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, AboutMe, Category
from projects.models import Project
from .utils import get_language_from_request, set_language_in_session

def home_view(request):
    """
    Main portfolio view that handles category selection and language switching
    """
    # Handle language switching
    if 'lang' in request.GET:
        lang = request.GET.get('lang')
        set_language_in_session(request, lang)
        # Keep lang in URL for consistency
        category = request.GET.get('category', 'about-me')
        # Don't redirect, just use the lang from GET
    
    # Get current language
    language = get_language_from_request(request)
    
    # Get selected category (default: about-me)
    category_slug = request.GET.get('category', 'about-me')
    
    # Get all categories for navigation
    all_categories = Category.objects.all().order_by('order')
    
    # Get profile mapped to the selected category
    profile = None
    category_obj = None
    
    # Try to find Category by slug
    try:
        category_obj = Category.objects.get(slug=category_slug)
        # Get first profile mapped to this category
        profile = category_obj.profiles.first()
    except Category.DoesNotExist:
        pass
    
    # Fallback to first profile if no mapping found
    if not profile:
        profile = Profile.objects.all().first()
    
    # Debug: ensure profile is available
    if not profile:
        # If still no profile, create a message for the template
        pass
    
    # Get projects
    projects = Project.objects.all().order_by('id')
    
    # Determine what content to show based on category
    content_data = {
        'category': category_slug,
        'language': language,
    }
    
    if category_slug == 'about-me':
        # About me uses profile content only
        pass
    elif category_slug == 'open-source':
        # Filter projects that are open source (has github_url) and linked to the profile
        if profile:
            content_data['projects'] = projects.filter(
                github_url__isnull=False
            ).exclude(
                github_url=''
            ).filter(
                profiles=profile
            )
        else:
            # If no profile, show all open source projects
            content_data['projects'] = projects.filter(github_url__isnull=False).exclude(github_url='')
    elif category_slug == 'education':
        # Education content - can be handled as a special category
        content_data['category'] = 'education'
    elif category_slug == 'skills':
        # Show all skills across all categories
        content_data['category'] = 'skills'
        # Get all categories that have skills text
        categories_with_skills = all_categories.filter(skills__isnull=False).exclude(skills='')
        content_data['categories_with_skills'] = categories_with_skills
    else:
        # For custom categories (cpp-developer, python-developer, ml-engineer, etc.)
        # Show projects linked to the profile for this category
        if category_obj:
            content_data['category'] = category_slug
            content_data['category_obj'] = category_obj
            # Get projects linked to the profile
            if profile:
                content_data['projects'] = projects.filter(profiles=profile)
            else:
                content_data['projects'] = projects.none()  # Empty queryset if no profile
        else:
            # Category not found
            content_data['category'] = category_slug
    
    context = {
        'profile': profile,
        'categories': all_categories,
        'current_category': category_slug,
        'current_language': language,
        'content_data': content_data,
    }
    
    return render(request, "home.html", context)

def profile_detail(request, slug):
    """Legacy profile detail view - kept for compatibility"""
    profile = get_object_or_404(Profile, slug=slug)
    projects = Project.objects.filter(profiles=profile)
    language = get_language_from_request(request)

    return render(request, "profiles/detail.html", {
        "profile": profile,
        "projects": projects,
        "language": language,
    })
