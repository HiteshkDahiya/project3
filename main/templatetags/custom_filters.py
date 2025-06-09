# templatetags/custom_filters.py
from django import template
register = template.Library()

@register.filter
def dict_get(d, key):
    return d.get(key, '')

@register.filter
def available_sizes_string(product, sizes):
    return ' '.join([f"{size}" for size in sizes if getattr(product, f'is_size{size}', False)])

@register.filter
def split(value, delimiter=' '):
    return value.split(delimiter)