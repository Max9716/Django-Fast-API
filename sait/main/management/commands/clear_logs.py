# myapp/management/commands/clear_logs.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from main.models import UserActionLog

class Command(BaseCommand):
    help = 'Удаляет логи старше 3 дней'

    def handle(self, *args, **kwargs):
        cutoff = timezone.now() - timedelta(days=1)
        deleted, _ = UserActionLog.objects.filter(timestamp__lt=cutoff).delete()
        self.stdout.write(f"Удалено {deleted} старых логов")
