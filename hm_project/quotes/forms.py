# from django.forms import ModelForm, CharField, ImageField, TextInput, FileInput

# from .models import Author

from django import forms
from .models import Author

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']