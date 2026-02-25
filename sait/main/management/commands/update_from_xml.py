from django.core.management.base import BaseCommand
from main.load_xml import load_from_xml
import logging

logging.basicConfig(filename='/home/ubuntu/sait/update_xml.log', level=logging.INFO)


class Command(BaseCommand):
    help = "Обновление базы данных из XML файлов"
    def handle(self, *args, **kwargs):
        load_from_xml()
        self.stdout.write(self.style.SUCCESS("✅ База обновлена из XML"))