from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _



class NewUserForm(UserCreationForm):
    email=forms.EmailField(required=True)

    class Meta:
        model=CustomUser
        fields=("username","email","password1","password2","gluten_trigger","lactose_trigger","nut_trigger")
    def save(self, commit=True):
        user=super(NewUserForm,self).save(commit=False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user
class AuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ("email", "password")

    # Checks if user credentials are valid
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Error when logging in!")

class CustomUserChangeForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ("gluten_trigger","lactose_trigger","nut_trigger")
    # def save(self, commit=True):
    #     user=super(CustomUserChangeForm,self).save(commit=False)
    #     user.email=self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #     return user