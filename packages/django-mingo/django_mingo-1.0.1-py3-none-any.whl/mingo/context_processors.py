from django.conf import settings

def mingo_theme(request):
    mingo_defined = hasattr(settings, 'MINGO_SETTINGS')
    if mingo_defined:
        mingo = settings.MINGO_SETTINGS
        default_theme = mingo['theme']
    else:
        default_theme = 'light'

    return {
        'default_theme': default_theme,
    }
