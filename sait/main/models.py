from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Flat (models.Model):
    id_flat = models.CharField("ID квартиры", max_length=20,primary_key=True)
    number = models.CharField("Номер квартиры", max_length=10, default="")
    number_on_floor = models.CharField("Номер на этаже", max_length=10, default="")
    complex = models.CharField("Комплекс", max_length=30, default="")
    id_complex = models.CharField("id комплекса", max_length=50, default="")
    house = models.CharField("Корпус", max_length=50, default="")
    id_house = models.CharField("id корпуса", max_length=50, default="")
    floor = models.CharField("Этаж", max_length=10, default="")
    section = models.CharField("Секция", max_length=10, default="")
    rooms = models.CharField("Комнат", max_length=10, default="")
    flat_type = models.CharField("Тип помещения", max_length=30, default="")
    price = models.CharField("Цена", max_length=20, default="")
    price_base = models.CharField("Базовая цена", max_length=20, default="")
    square = models.CharField("Площадь", max_length=10, default="")
    square_live = models.CharField("Площадь жилая", max_length=10, default="")
    square_hook = models.CharField("Площадь кухни", max_length=10, default="")
    status = models.CharField("Статус", max_length=10, default="")
    decoration = models.CharField("Отделка", max_length=10, default="")
    plan = models.CharField("Планировка", max_length=250, default="")
    floor_plan = models.CharField("Поэтажка", max_length=250, default="")

    def __str__(self):
        return self.number
    class Meta:
        verbose_name = "Квартира"
        verbose_name_plural = "Квартиры"

    objects = models.Manager()

class Application(models.Model):
    type = models.CharField("Тип заявки", max_length=30)
    name = models.CharField("Имя клиента", max_length=30)
    date = models.DateField("Дата заявки")
    def __str__(self):
        return self.type
    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

class UserActionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)  # описание действия
    path = models.CharField(max_length=255, blank=True)  # URL страницы
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} — {self.action} ({self.timestamp})"