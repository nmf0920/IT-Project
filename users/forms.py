from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
import re

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserPasswordResetForm(PasswordResetForm):
    username = forms.CharField()
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[0-9a-zA-Z]+$', username):
            raise forms.ValidationError("Username must contain letters and numbers only.")
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("User does not exist")
        return username

    def clean_new_password(self):
        username = self.cleaned_data.get('username')
        new_password = self.cleaned_data.get('new_password')

        if len(new_password) < 8:
            raise forms.ValidationError("New password must be at least 8 characters long.")

        if 'username' not in self.errors:  # Add this line
            user = User.objects.get(username=username)
            if user.check_password(new_password):
                raise forms.ValidationError("New password is the same as the current one")
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password:
            if new_password != confirm_password:
                self.add_error('confirm_password', "New password and Confirm password do not match")

        return cleaned_data

    def save(self, commit=True):
        username = self.cleaned_data.get('username')
        new_password = self.cleaned_data.get('new_password')
        user = User.objects.get(username=username)
        user.set_password(new_password)
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']