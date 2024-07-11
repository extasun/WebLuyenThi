from django import forms
from .models import StudentUser

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = StudentUser
        fields = ['username', 'password', 'first_name', 'last_name']
        widgets={
            'username': forms.TextInput(attrs={'class':'form-control', 'tabindex':'1', 'placeholder':'Username'}),
            'first_name': forms.TextInput(attrs={'class':'form-control', 'tabindex':'1', 'placeholder':'First Name', 'required':'true'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'tabindex':'1', 'placeholder':'Last Name', 'required':'true'}),
            'password': forms.PasswordInput(attrs={'class':'form-control', 'tabindex':'1', 'placeholder':'Password', 'required':'true'}),
        }