from django import forms
from .models import Rental

class RentalForm(froms.ModelForm):
    class Meta:
        model = Rental
        fields = ("")
        widgets = {
            
        }