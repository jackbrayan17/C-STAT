from django.core.management.base import BaseCommand
from fast.models import User

class Command(BaseCommand):
    help = 'Create default admin user'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin1234', role='Admin')
            self.stdout.write(self.style.SUCCESS('Admin user created!'))
