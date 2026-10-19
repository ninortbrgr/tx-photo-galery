from django.contrib import admin
from django import forms
from .models import Gallery, MediaItem

# Multiple File Upload
class MediaItemAdminForm(forms.ModelForm):
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False,
        label="Dateien (Fotos/Videos)"
    )

    class Meta:
        model = MediaItem
        fields = ['file', 'title']

class MediaItemInline(admin.TabularInline):
    model = MediaItem
    form = MediaItemAdminForm
    extra = 1

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'category')
    list_filter = ('category', 'date')
    search_fields = ('title', 'description')
    inlines = [MediaItemInline]

    # Override the save_formset method to handle multiple file uploads
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        
        # Save each instance and handle multiple file uploads
        for obj in instances:
            obj.save()
            
        # Handle multiple file uploads for the MediaItemInline
        for file in request.FILES.getlist('media_items-0-file'):
            MediaItem.objects.create(gallery=form.instance, file=file)
            
        formset.save_m2m()