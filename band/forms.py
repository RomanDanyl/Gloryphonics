from django import forms
from django.contrib import admin

from band.models import Band
from user.models import User


class BandAdminForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple("Members", is_stacked=False),
    )

    class Meta:
        model = Band
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["members"].initial = User.objects.filter(band=self.instance)

    def save(self, commit=True):
        band = super().save(commit=False)
        if commit:
            band.save()
        User.objects.filter(band=band).update(band=None)
        self.cleaned_data["members"].update(band=band)
        return band
