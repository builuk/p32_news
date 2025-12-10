# news/forms.py
from django import forms
from .models import Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3})
        }


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class WeatherForm(forms.Form):
    city = forms.CharField(
        max_length=100,
        label='Місто',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введіть назву міста',
            'class': 'form-control'
        })
    )