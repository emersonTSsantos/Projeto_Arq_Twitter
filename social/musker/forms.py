from django import forms
from .models import Meep
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", required=True, widget=forms.TextInput(
        attrs={
            'class': "form-control",
            'placeholder': 'Digite seu email'
        }
    ))

    first_name = forms.CharField(label="", max_length=100, required=True, widget=forms.TextInput(
        attrs={
            'class': "form-control",
            'placeholder': 'Digite seu primeiro nome'
        }
    ))

    last_name = forms.CharField(label="", max_length=100, required=True, widget=forms.TextInput(
        attrs={
            'class': "form-control",
            'placeholder': 'Digite seu sobrenome'
        }
    ))

    class Meta:
        model = User
        fields = (  
                    'username', 
                    'email', 
                    'first_name', 
                    'last_name', 
                    'password1', 
                    'password2'
                )
        
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Digite seu nome de usuário'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small class="text-white">Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Digite sua senha'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted"><small class="text-white"><li>Sua senha não pode ser muito parecida com outras informações pessoais.</li><li>Sua senha deve ter pelo menos 8 caracteres.</li><li>Não pode ser uma senha muito comum.</li></small></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirme sua senha'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small class="text-white">Digite a mesma senha novamente, para verificação.</small></span>'