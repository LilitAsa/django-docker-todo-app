import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import UserProfile, Task


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "phone", "password1", "password2"]

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not re.match(r'^\+?\d{10,15}$', phone):
            raise forms.ValidationError("Введите корректный номер телефона (10-15 цифр, можно с +).")
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        
        if commit:
            user.save()
            
            UserProfile.objects.create(
                user=user,
                phone=self.cleaned_data["phone"],
                first_name=self.cleaned_data["first_name"],
                last_name=self.cleaned_data["last_name"],
                email=self.cleaned_data["email"]
            )
        return user
    
    
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField()
    
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Телефон'}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'is_urgent', 'is_important']

    is_urgent = forms.BooleanField(required=False)
    is_important = forms.BooleanField(required=False)

    def save(self, commit=True):
        task = super().save(commit=False)
        task.check_flags()  # Call the method to check flags after saving
        if commit:
            task.save()
        return task