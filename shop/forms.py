from django import forms

class CartAddForm(forms.Form):
    quantity=forms.IntegerField(label='تعداد',min_value=1,max_value=5,widget=forms.NumberInput(attrs={'class': 'form-row input-text'}))
    