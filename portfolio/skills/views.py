from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from profiles.models import Category
from profiles.utils import get_language_from_request

@require_http_methods(["GET"])
def console_output(request, category_slug):
    """
    API endpoint that returns formatted skill output for a category
    Mimics: cat skills_<category>.txt
    """
    language = get_language_from_request(request)
    
    try:
        category_obj = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        return JsonResponse({
            'error': f'Category "{category_slug}" not found'
        }, status=404)
    
    # Check if category has skills text
    if not category_obj.skills or not category_obj.skills.strip():
        return JsonResponse({
            'error': f'Category "{category_slug}" does not have skills',
            'is_special': True
        }, status=404)
    
    # Format output - just the skills content (cd and cat commands are handled in JS)
    output_lines = []
    output_lines.append("")
    
    # Split skills text by lines and format
    skills_lines = category_obj.skills.strip().split('\n')
    for line in skills_lines:
        line = line.strip()
        if line:
            # If line doesn't start with bullet, add one
            if not line.startswith('•') and not line.startswith('-') and not line.startswith('*'):
                output_lines.append(f"  • {line}")
            else:
                output_lines.append(f"  {line}")
    
    output_lines.append("")
    output_lines.append(f"C:\\{category_slug}>")
    
    return JsonResponse({
        'output': '\n'.join(output_lines),
        'category': category_obj.get_name(language),
        'language': language
    })
