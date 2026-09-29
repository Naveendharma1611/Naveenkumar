from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from apps.accounts.models import Role, StudentProfile, User
from apps.contact.models import ContactMessage


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"autofocus": True}))


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["full_name", "email"]

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = Role.STUDENT
        if commit:
            user.save()
            StudentProfile.objects.create(user=user)
        return user


class AccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["full_name", "avatar"]


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 6})}
