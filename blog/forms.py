from django import forms

class ContactForm(forms.Form):
    email = forms.EmailField(required=True, label='E-mail Adresiniz')
    konu = forms.CharField(required=True)
    mesaj = forms.CharField(widget=forms.Textarea, required=True)
