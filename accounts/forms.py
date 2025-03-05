from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control"}))

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        required=True
    )
    
    class Meta:
        model = User
        fields = ("email", "password1", "password2")
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email này đã được sử dụng. Vui lòng sử dụng email khác.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        # Gán username = email để đảm bảo trường username không rỗng và duy nhất
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user