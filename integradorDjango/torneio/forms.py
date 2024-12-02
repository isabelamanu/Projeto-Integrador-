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
