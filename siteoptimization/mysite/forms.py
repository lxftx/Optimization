from django import forms
from .models import *

class FormInputData(forms.ModelForm):
    class Meta:
        model = InputData
        fields = "__all__"


class FormOgranichenie(forms.ModelForm):
    class Meta:
        model = Ogranichenie
        fields = "__all__"