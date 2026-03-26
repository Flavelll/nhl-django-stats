from django import forms
from .models import Session

class FilterForm(forms.Form):
    session = forms.ModelChoiceField(
        queryset=Session.objects.filter(session_type__in=["Race", "Qualifying", "Practice"]).order_by("-date_start"),
        required=True,
        label="Race",
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )

    drivers = forms.MultipleChoiceField(
        choices=[],
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Drivers"
    )

    def __init__(self, *args, **kwargs):
        driver_choices = kwargs.pop("driver_choices", [])
        super().__init__(*args, **kwargs)
        self.fields["drivers"].choices = driver_choices
