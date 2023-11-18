from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from esign.models import Organization

CustomUser = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser from CustomUser model'

    def handle(self, *args, **options):
        username = 'eee'
        email = 'eee@eee.com'
        password = 'eee'
        org_id = 'COM003'
        position = 'Company Secretary'

        # Get or create an Organization instance
        org_instance, created = Organization.objects.get_or_create(orgID=org_id)

        # Create a new CustomUser object
        new_superuser = CustomUser.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            orgID=org_instance,
            position=position
        )

        # Set the password for the superuser
        new_superuser.set_password(password)
        new_superuser.save()

        self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
