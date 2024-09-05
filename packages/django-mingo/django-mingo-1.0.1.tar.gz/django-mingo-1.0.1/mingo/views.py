from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import logout
# Create your views here.

def logout_view(request):
    logout(request)
    return redirect('/admin/logout/')

def theme_change(request):
    theme = request.GET.get('theme')
    if theme == 'dark':
        request.session['theme'] = 'dark'
        return JsonResponse({'success': True, 'theme': 'dark'})
    elif theme == 'light':
        request.session['theme'] = 'light'
        return JsonResponse({'success': True, 'theme': 'light'})