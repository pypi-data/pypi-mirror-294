from django.contrib import admin
from django import forms
from django.contrib.admin import AdminSite
from .forms import CustomAuthenticationForm, BaseAdminForm, MingoUserAddForm, MingoUserChangeForm
from django.contrib.admin import ModelAdmin
from django.urls import NoReverseMatch, Resolver404, resolve, reverse
from django.contrib.auth.admin import UserAdmin


#Change the default login form
AdminSite.login_form = CustomAuthenticationForm

#Change the default change form for model
ModelAdmin.form = BaseAdminForm

#Change the user adding form
UserAdmin.add_form = MingoUserAddForm
UserAdmin.form = MingoUserChangeForm


#Add class to related field like foreignkey select field
def change_formfield_for_foreignkey(original_method):
    def wrapper(self, db_field, request, **kwargs):
        kwargs["widget"] = forms.Select(attrs={"class": "form-select"})
        return original_method(self, db_field, request, **kwargs)
    return wrapper
ModelAdmin.formfield_for_foreignkey = change_formfield_for_foreignkey(ModelAdmin.formfield_for_foreignkey)






