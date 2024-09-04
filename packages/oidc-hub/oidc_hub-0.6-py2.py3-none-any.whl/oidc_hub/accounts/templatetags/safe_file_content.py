from django import template
from django.contrib.staticfiles import finders
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def safe_file_content(file_path):
    content = ""
    if static_file := finders.find(file_path):
        with open(static_file, "r") as file:
            content = file.read()
    return mark_safe(content)
