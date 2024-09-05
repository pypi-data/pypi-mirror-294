# In yourapp/widgets.py

from django.contrib.admin.widgets import AdminTextInputWidget

class MingoTextInputWidget(AdminTextInputWidget):
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'vTextField form-control',  # Add your custom classes here
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)
