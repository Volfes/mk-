from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(max_length=200)
    first_name = forms.CharField(max_length=50, label="Imię")
    last_name = forms.CharField(max_length=50, label="Nazwisko")
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
        'password2')
        labels = {
            "password1": "Hasło", 
            'username': 'Nazwa użytkownika', 
            'password2': 'Powtórz hasło',
            }
        error_messages = {
        'username': {
            "required": "Podaj nazwę użytkownika",
            "max_length": "Maksymalna długość nazwy użytkownika to 100 znaków"
        },
        'email': {
            "required": "Podaj email",
            "max_length": "Maksymalna długość nazwy email to 200 znaków"
        },
        'first_name': {
            "required": "Podaj imię",
        },
        'last_name': {
            "required": "Podaj nazwisko",
        },
        'password1': {
            "required": "Podaj hasło",
        },
        'password2': {
            "required": "Powtórz hasło",
        }
            }

    #override labels for passwords
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, v in self.Meta.labels.items():
            self[k].label = v


class PasswordChangeFormLabelUpdate(PasswordChangeForm):

    class Meta:
        fields = ("old_password", "new_password1", "new_password2")
        labels = {
            "old_password": "Stare hasło", 
            'new_password1': 'Nowe hasło', 
            'new_password2': 'Powtórz nowe hasło',
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, v in self.Meta.labels.items():
            self[k].label = v



class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True, label=('Podaj nowy adres email:'))

    class Meta:
        model = User
        fields = ("email",)

