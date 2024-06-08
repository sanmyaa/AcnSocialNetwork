from django.db import models
from rest_framework.serializers import ValidationError
from typing import Type


class TimeStampable(models.Model):
    """
    Abstract model that provides timestamp fields for creation and modification.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def check_unique_relation(
    obj: models.Model,
    *,
    model: Type[models.Model],
    label: str,
    from_user_model_field: str = "from_user",
    to_user_model_field: str = "to_user",
    from_user_obj_field: str = "from_user",
    to_user_obj_field: str = "to_user",
) -> None:
    """
    Check for the uniqueness of a relationship between users in a given model.
    Args:
        obj (models.Model): The instance of the model being checked.
        model (Type[models.Model]): The model class to check against.
        label (str): The label for the ValidationError.
        from_user_model_field (str, optional): The field name for sender in model.
        to_user_model_field (str, optional): The field name for recipient in model.
        from_user_obj_field (str, optional): The field name for sender in obj.
        to_user_obj_field (str, optional): The field name for recipient in obj.
    Raises:
        ValidationError: If a relationship already exists in either direction.
    """
    if model.objects.filter(
        **{
            from_user_model_field: getattr(obj, from_user_obj_field, None),
            to_user_model_field: getattr(obj, to_user_obj_field, None),
        }
    ).exists():
        raise ValidationError({label: ["exists (was sent)"]})
    elif model.objects.filter(
        **{
            from_user_model_field: getattr(obj, to_user_obj_field, None),
            to_user_model_field: getattr(obj, from_user_obj_field, None),
        }
    ).exists():
        raise ValidationError({label: ["exists (was received)"]})
