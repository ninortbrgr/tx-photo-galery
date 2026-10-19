from django import forms
from .models import Gallery


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]
        return [single_file_clean(data, initial)]


class GalleryAdminForm(forms.ModelForm):
    new_files = MultipleFileField(required=False, label="Dateien (Fotos/Videos)")

    class Meta:
        model = Gallery
        fields = "__all__"