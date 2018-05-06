from django import forms
from .models import ScrumyGoals

class ChangeTaskStatusForm(forms.ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['status_id']
