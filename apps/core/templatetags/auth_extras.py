from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter(name='has_any_group')
def has_any_group(user, group_names):
    """
    Usage: {% if user|has_any_group:"Group A,Group B,Group C" %}
    """
    groups = [g.strip() for g in group_names.split(',')]
    return user.groups.filter(name__in=groups).exists()
