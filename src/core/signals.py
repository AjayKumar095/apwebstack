# core/signals.py
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.apps import apps
from .models import Media

@receiver(pre_delete, sender=Media)
def delete_media_cleanup(sender, instance, **kwargs):
    """
    When a Media object is deleted:
    1. Delete the physical file from disk.
    2. Nullify all ForeignKey references pointing to this file.
    """

    # 1️⃣ Delete file from disk
    try:
        instance.file.delete(save=False)
    except Exception as e:
        print("File delete error:", e)

    # 2️⃣ Find all models that use Media as FK and set them to NULL
    all_models = apps.get_models()

    for model in all_models:
        for field in model._meta.get_fields():

            # Check only for FK fields pointing to Media
            if field.is_relation and field.many_to_one and field.related_model == Media:
                field_name = field.name

                # Set FK field to NULL where it matches this media
                try:
                    model.objects.filter(**{field_name: instance}).update(**{field_name: None})
                except Exception as e:
                    print("Cleanup FK error:", e)
