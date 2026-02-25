import os
from lxml import etree
from django.conf import settings
from .models import Flat

XML_FOLDER = os.path.join(settings.BASE_DIR, "main", "base_flat")


def load_from_xml(filename=None):
    xml_ids = set()
    files_to_process = [filename] if filename else os.listdir(XML_FOLDER)

    for file in files_to_process:
        if not file.endswith(".xml"):
            continue

        filepath = os.path.join(XML_FOLDER, file)

        try:
            # stream-парсинг
            context = etree.iterparse(filepath, events=("end",), tag="Квартира", encoding="utf-8-sig")
            for event, item in context:
                try:
                    id_flat = item.get("id")
                    if not id_flat:
                        item.clear()
                        continue
                    xml_ids.add(str(id_flat))

                    def get_text(tag):
                        el = item.find(tag)
                        return el.text.strip() if el is not None and el.text else ""

                    data = {
                        "number": get_text("Номер"),
                        "number_on_floor": get_text("НомерНаЭтаже"),
                        "complex": get_text("Комплекс"),
                        "id_complex": get_text("КомплексID"),
                        "house": get_text("Корпус"),
                        "id_house": get_text("КорпусID"),
                        "floor": get_text("Этаж"),
                        "section": get_text("Секция"),
                        "rooms": get_text("Комнат"),
                        "flat_type": get_text("ТипПомещений"),
                        "price": get_text("СтоимостьСоСкидкой"),
                        "price_base": get_text("СтоимостьБазовая"),
                        "square": get_text("Площадь"),
                        "square_live": get_text("ПлощадьЖил"),
                        "square_hook": get_text("ПлощадьКух"),
                        "status": get_text("Статус"),
                        "decoration": get_text("Отделка"),
                        "plan": get_text("Планировка"),
                        "floor_plan": get_text("Поэтажка"),
                    }

                    Flat.objects.update_or_create(
                        id_flat=str(id_flat),
                        defaults=data
                    )

                except Exception as e:
                    print(f"Ошибка при обработке квартиры {id_flat}: {e}")
                finally:
                    item.clear()
                    while item.getprevious() is not None:
                        del item.getparent()[0]

            del context

        except Exception as e:
            print(f"Ошибка при обработке {file}: {e}")

    if not filename:
        Flat.objects.exclude(id_flat__in=xml_ids).delete()
