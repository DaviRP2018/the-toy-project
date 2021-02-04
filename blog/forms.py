from django import forms
from django.contrib.auth.models import User


class WriterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]
        widgets = {
            'password': forms.PasswordInput(),
        }

    username = forms.CharField(max_length=255)
    password = forms.PasswordInput()
    is_editor = forms.BooleanField(label="I'm an editor", required=False)
