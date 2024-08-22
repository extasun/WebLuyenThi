from django import forms
from .models import CauHoi
class SubjectSelectionForm(forms.Form):
    subjects = forms.MultipleChoiceField(
        choices=CauHoi.SUBJECT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )