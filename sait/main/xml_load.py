import requests
import xml.etree.ElementTree as ET
from io import BytesIO
import datetime
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from lxml import etree
from .load_xml import load_from_xml

global domcklik



domcklik = False
def strip_namespace(elem):
    for el in elem.iter():
        if '}' in el.tag:
            el.tag = el.tag.split('}', 1)[1]
def tag_values_domcklik(node, x, **tag):
    tags_chain = tag[x]['tags']
    number = int(tag[x].get("number", 0))
    current = node
    for t in tags_chain:
        if t.startswith(".."):
            steps = t.count("..")
            for _ in range(steps):
                current = current.getparent()
                if current is None:
                    return ""
        else:
            found_all = current.findall(t)
            if not found_all:
                return ""
            current = found_all[number] if number < len(found_all) else found_all[-1]
    return current.text.strip() if current.text else ""
def tag_values(node, x, **tag):
    tags_chain = tag[x]['tags']
    name = tag[x]["attrs"]["name"]
    value = tag[x]["attrs"]["values"]
    number = int(tag[x].get("number", 0))
    if x == "flat_id" and name:
        return node.attrib.get(name, "")
    current = node
    for i, t in enumerate(tags_chain):
        if i == len(tags_chain) - 1:
            found_all = current.findall(t)
            if not found_all:
                return ""
            if name and value:
                filtered = [f for f in found_all if f.attrib.get(name) == value]
                if not filtered:
                    return ""
                if number > 0:
                    current = filtered[number] if number < len(filtered) else filtered[-1]
                else:
                    current = filtered[0]
                return current.text.strip() if current.text else ""
            if name:
                if number > 0:
                    current = found_all[number] if number < len(found_all) else found_all[-1]
                else:
                    current = found_all[0]
                return current.attrib.get(name, "")
            if number > 0:
                current = found_all[number] if number < len(found_all) else found_all[-1]
            else:
                current = found_all[0]
            return current.text.strip() if current.text else ""
        found_all = current.findall(t)
        if not found_all:
            return ""
        if number > 0:
            current = found_all[number] if number < len(found_all) else found_all[-1]
        else:
            current = found_all[0]
    if name:
        return current.attrib.get(name, "")
    return current.text.strip() if current.text else ""
def process_offer(offer, tag):
    flat = {}
    if domcklik == False:
        for key in tag:
            flat[key] = tag_values(offer, key, **tag)
        flat["type_room"] = (flat.get("type_room", "") or "") + (flat.get("rooms", "") or "")
    else:
        for key in tag:
            flat[key] = tag_values_domcklik(offer, key, **tag)
        flat["type_room"] = (flat.get("type_room", "") or "") + (flat.get("rooms", "") or "")
    return flat

def xml_load(url, id, **tag):
    global domcklik
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        tree = etree.parse(BytesIO(response.content))
        root_xml = tree.getroot()
        strip_namespace(root_xml)

        offers = root_xml.findall(f".//{tag['parents'][-1]}")
        tag_for_threads = tag.copy()
        tag_for_threads.pop('parents', None)
        flats = []

        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(process_offer, offer, tag_for_threads) for offer in offers]
            for f in as_completed(futures):
                flats.append(f.result())

        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        root = ET.Element('root', date=date)

        for l in flats:
            flatID = ET.SubElement(root, "Квартира", id=str(l.get("flat_id")))
            fields = [
                ("number", "Номер"), ("complex", "Комплекс"), ("complex_id", "КомплексID"),
                ("house", "Корпус"), ("house_id", "КорпусID"), ("floor", "Этаж"), ("section", "Секция"),
                ("rooms", "Комнат"), ("type_room", "ТипПомещений"), ("price", "СтоимостьСоСкидкой"),
                ("price_base", "СтоимостьБазовая"), ("area", "Площадь"), ("areaH", "ПлощадьЖил"),
                ("areaK", "ПлощадьКух"), ("status", "Статус"), ("plan", "Планировка"),
                ("floor_plan", "Поэтажка")
            ]
            for key, xml_tag in fields:
                ET.SubElement(flatID, xml_tag).text = str(l.get(key, ""))

        mydata = ET.tostring(root, encoding='utf-8')
        safe_id = re.sub(r'[<>:"/\\|?*]', '_', str(id))
        with open(f"/home/ubuntu/sait/main/base_flat/{id}.xml", "wb") as myfile:
            myfile.write(mydata)

        load_from_xml(filename=f"{id}.xml")

        return id, True

    except Exception as e:
        print("Ошибка:", e)
        return id, False