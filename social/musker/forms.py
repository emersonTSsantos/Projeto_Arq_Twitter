from django import forms
from .models import Meep

class MeepForm(forms.ModelForm):
    body = forms.CharField(required=True, widget=forms.Textarea(
        attrs={
                'class': "form-control", 
                'placeholder': 'No que você está pensando?',
                'rows': 3,
                'maxlength': 280,
                'style': 'resize: none;'
            }
        ),
        label="")

    class Meta:
        model = Meep
        exclude = ("user", "created_at", "updated_at")
