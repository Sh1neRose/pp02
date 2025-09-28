from django import forms

class SubscribeForm(forms.Form):
    email = forms.EmailField(
        required=True,
        max_length=66,
        label='',
        widget=forms.EmailInput(attrs={'placeholder': 'Your email...'})
        )

class UnsubscribeForm(forms.Form):
    email = forms.EmailField(
        required=True,
        max_length=66,
        label='',
        widget=forms.EmailInput(attrs={'placeholder': 'Your email...'})
        )