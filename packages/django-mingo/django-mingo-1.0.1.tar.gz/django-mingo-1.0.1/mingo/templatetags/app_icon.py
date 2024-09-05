from django import template
from django.apps import apps

register = template.Library()

@register.filter
def get_app_icon(app):
    app_config = apps.get_app_config(app['app_label'])
    return getattr(app_config, 'icon', 'ki-home-1')

# @register.filter
# def match_app_url(request, app):
#     current_url = request.build_absolute_uri()
#     if 
