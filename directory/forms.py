from django import forms
from django.contrib.auth.models import User


class ReceptionRegistrationForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "name"}),
    )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "new-password"}),
    )
    confirm_password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "new-password"}),
    )

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if User.objects.filter(username__iexact=name).exists():
            raise forms.ValidationError("This name is already registered.")
        return name

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class DataUploadForm(forms.Form):
    upload_file = forms.FileField(
        label="Excel or CSV file",
        help_text="Accepted formats: .xlsx or .csv",
    )

    def clean_upload_file(self):
        upload_file = self.cleaned_data["upload_file"]
        filename = upload_file.name.lower()

        if not filename.endswith((".xlsx", ".csv")):
            raise forms.ValidationError("Please upload an .xlsx or .csv file.")

        return upload_file


class ManualOrganizerForm(forms.Form):
    district = forms.CharField(
        max_length=120,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Optional district name"}),
        help_text="Leave empty to auto-detect district from place names.",
    )
    organizer = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Organizer name"}),
    )
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone number"}),
    )
    locations = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 7,
                "placeholder": "Paste comma-separated locations",
            }
        )
    )
    aliases = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Optional comma-separated aliases in same order, e.g. ഒളവട്ടൂർ, കോഴിക്കോട്",
            }
        ),
    )

    def clean_locations(self):
        locations = [
            location.strip()
            for location in self.cleaned_data["locations"].split(",")
            if location.strip()
        ]
        if not locations:
            raise forms.ValidationError("Enter at least one location.")
        return locations

    def clean_aliases(self):
        aliases = self.cleaned_data.get("aliases", "")
        return [alias.strip() for alias in aliases.split(",")]
