import os
from django import template
register = template.Library()
@register.filter
def basename(value):
   """Extracts the base name of the file from its full path."""
   return os.path.basename(value)