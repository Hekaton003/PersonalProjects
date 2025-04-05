from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=254, required=True)
    last_name = forms.CharField(max_length=254, required=True)
    country = forms.CharField(required=True)
    city = forms.CharField(required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    phone = forms.CharField(required=True)
    zipcode = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2',
                  'country', 'city', 'address', 'phone', 'zipcode']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            profile,created = Profile.objects.update_or_create(
                user=user,
                defaults={
                    'country': self.cleaned_data['country'],
                    'city': self.cleaned_data['city'],
                    'address': self.cleaned_data['address'],
                    'phone': self.cleaned_data['phone'],
                    'zipcode': self.cleaned_data['zipcode']
                })
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=254)
    last_name = forms.CharField(max_length=254)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'country', 'city', 'address', 'phone', 'zipcode']
