from django import forms

class NewsFilterForm(forms.Form):
    start_date = forms.DateField(label='От', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='До', required=False, widget=forms.DateInput(attrs={'type': 'date'}))