from django import forms
from .models import Marks

# Define the form class to edit a Marks record
class EditMarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = ['student', 'subject', 'marks', 'grade']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap 'form-control' class to all fields
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'  # Add Bootstrap class to each field
            })