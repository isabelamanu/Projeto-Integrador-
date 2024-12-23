from django import forms

class ConfigForm(forms.Form):
    numero = forms.IntegerField(
        min_value=2, 
        widget=forms.NumberInput(attrs={"step": 2}),
        label="Quantos jogadores? (par)"
    )

    def clean_numero(self):
        numero = self.cleaned_data["numero"]
        if numero & (numero - 1) != 0:  # Verifica se é potência de 2
            raise forms.ValidationError("O número deve ser uma potência de 2.")
        return numero


class JogadoresForm(forms.Form):
    def __init__(self, *args, **kwargs):
        numero = kwargs.pop('numero', 0)
        super(JogadoresForm, self).__init__(*args, **kwargs)

        for i in range(1, numero + 1):
            self.fields[f'jogador_{i}'] = forms.CharField(label=f"Jogador {i}", max_length=100, required=True)


class LoginForms(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label = 'confirm password', widget = forms.PasswordInput)

    def cleanpassword(self):
        data = self.cleaned_data
        password = self.cleaned_data('password')
        password2 = self.cleaned_data('password2')
        if password != password2:
            raise forms.ValidationError('the passwords should be equals')
        return data
