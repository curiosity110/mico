from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from django.db import transaction

from accounts.models import GroupDescription


class Command(BaseCommand):
    help = 'Create the default permission groups for the application'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        groups = self.get_groups()

        for group_name, description in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                GroupDescription.objects.create(group=group, description=description)
                self.stdout.write(self.style.SUCCESS(f'Created group: {group_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Group already exists: {group_name}'))

    def get_groups(self) -> dict[str, str]:
        return {
            'PredictionAgent': 'Can view and manage prediction orders assigned to them',
            'PendingAgent': 'Can view and manage pending orders assigned to them',
            'InventoryManager': 'Can manage inventory and products',
            'Administrator': 'Can view and manage all aspects of the application',
        }
