from django         import forms
from django.core    import validators


class AnimalForm( forms.Form ):

    animal = forms.CharField( max_length = 50 )
    name   = forms.CharField( max_length = 50 )
    age    = forms.FloatField( min_value = 0, max_value = 200 )


    def clean(self):
        user_cleaned_data = super().clean()