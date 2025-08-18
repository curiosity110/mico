from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseInternalModel


# Create your models here.
class User(BaseInternalModel, AbstractUser):
    pass
    # is_active = models.BooleanField(
    #     _("active"),
    #     default=True,
    #     help_text=_(
    #         "Designates whether this user should be treated as active. "
    #         "Unselect this instead of deleting accounts."
    #     ),
    #     db_index=True,
    # )


class GroupDescription(BaseInternalModel):
    group = models.OneToOneField(
        "auth.Group", on_delete=models.CASCADE, related_name="description"
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.group.name} - {self.description}"
