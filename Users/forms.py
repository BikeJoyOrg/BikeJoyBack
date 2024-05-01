from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

    def save(self, commit=True):
        # Obtener el último ID en la tabla de CustomUser
        last_id = CustomUser.objects.last().id if CustomUser.objects.exists() else 0
        # Asignar el siguiente ID disponible
        self.instance.id = last_id + 1
        # Guardar el usuario
        return super().save(commit)
