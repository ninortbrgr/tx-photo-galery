from django.db import models
from django.contrib.auth.models import Group

class Gallery(models.Model):
    # Dropdown choices for the category field
    CATEGORY_CHOICES = [
        ('team-26/27', 'Team Photo 2026/2027pip'),
        
    ]

    title = models.CharField(max_length=75, verbose_name="Titel")
    description = models.TextField(blank=True, max_length=225, verbose_name="Beschreibung")
    date = models.DateField(verbose_name="Datum")
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        default='team', 
        verbose_name="Kategorie"
    )
    def __str__(self):
        return self.title

    allowed_groups = models.ManyToManyField(
        Group, 
        blank=True, 
        verbose_name="Erlaubte Gruppen",
        help_text="Wähle aus, welche Gruppen diese Galerie sehen dürfen (leer lassen = für alle eingeloggten Gruppen? Oder spezifisch)."
    )

    def __str__(self):
        return self.title

class MediaItem(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='photos', verbose_name="Galerie")
    file = models.FileField(upload_to='gallery-media/team-photo26-27/', verbose_name="Dateiupload (Foto/Video)")
    title = models.CharField(max_length=100, blank=True, verbose_name="Bildtitel - Optional")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Hochgeladen am")

    def __str__(self):
        return self.title if self.title else f"Bild {self.id}"