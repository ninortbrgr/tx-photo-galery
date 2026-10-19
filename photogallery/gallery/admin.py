from django.contrib import admin
from .forms import GalleryAdminForm
from .models import Gallery, MediaItem


class MediaItemInline(admin.TabularInline):
    model = MediaItem
    extra = 0   # normales Form, kein multiple-Hack mehr


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    form = GalleryAdminForm
    list_display = ("title", "date", "category")
    list_filter = ("category", "date")
    search_fields = ("title", "description")
    inlines = [MediaItemInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        for f in form.cleaned_data.get("new_files") or []:
            if f:
                MediaItem.objects.create(
                    gallery=form.instance,   # Name deines ForeignKeys anpassen!
                    file=f,
                    title=f.name,            # oder was auch immer dein title braucht
                )