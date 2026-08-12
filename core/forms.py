from django import forms
from .models import RegistroUso


class SolicitarVeiculoForm(forms.ModelForm):
    class Meta:
        model = RegistroUso
        # Selecionamos apenas os campos que o motorista precisa preencher na hora de pedir
        fields = ['veiculo', 'km_inicial', 'observacoes']
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-control'}),
            'km_inicial': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 45000'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Destino, motivo, etc.'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra o campo veiculo para mostrar apenas os disponiveis
        self.fields['veiculo'].queryset = self.fields['veiculo'].queryset.filter(
            disponivel=True)


class FinalizarUsoForm(forms.ModelForm):
    class Meta:
        model = RegistroUso
        # Na devolução, solicitamos apenas o KM Final e permitimos atualizar as observações
        fields = ['km_final', 'observacoes']
        widgets = {
            'km_final': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 45150'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observações do retorno, avarias, etc.'}),
        }

    def clean_km_final(self):
        km_final = self.cleaned_data.get('km_final')
        km_inicial = self.instance.km_inicial

        # Validação: KM Final não pode ser menor que o KM Inicial!
        if km_final and km_final < km_inicial:
            raise forms.ValidationError(
                f"O KM Final ({km_final}) não pode ser menor que o KM Inicial ({km_inicial}).")

        return km_final
