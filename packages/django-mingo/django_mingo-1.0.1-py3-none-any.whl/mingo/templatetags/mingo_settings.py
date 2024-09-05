from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def get_settings(key):
    mingo_defined = hasattr(settings, 'MINGO_SETTINGS')
    if mingo_defined:
        mingo = settings.MINGO_SETTINGS
        return mingo.get(key, '')
    else: 
        return None