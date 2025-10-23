from django import forms
from .models import Usuario


class RegistroForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=True)
    apellido = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput, required=True, label='Confirmar contraseña')
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Las contraseñas no coinciden')
        
        # Verificar si el email ya existe
        email = cleaned_data.get('email')
        if email and Usuario.objects.filter(email=email).exists():
            self.add_error('email', 'Este correo electrónico ya está registrado')
        
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        
        # En un sistema real, verificaríamos la contraseña aquí
        if email and not Usuario.objects.filter(email=email).exists():
            self.add_error('email', 'No existe un usuario con este correo electrónico')
        
        return cleaned_data