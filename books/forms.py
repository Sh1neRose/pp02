from django import forms

class Search(forms.Form):
    query = forms.CharField(
        required=True,
        max_length=100,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your query...'})
    )
