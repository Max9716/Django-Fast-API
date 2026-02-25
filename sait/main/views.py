from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Application
from .forms import ApplicationForm
from .models import Flat
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .xml_load import xml_load


# Create your views here.
class NewFlat(DetailView):
    model = Flat
    template_name = 'main/flat.html'
    context_object_name = "flat"
#@login_required
def index(request):
    return render(request, "main/default.html")
@login_required
def news(request):
    return render(request, "main/news.html")
@login_required
def flat(request):
    sort = request.GET.get('sort', 'price')  # сортировка по умолчанию — по цене
    order = request.GET.get('order', 'asc')

    flats = Flat.objects.all()

    rooms = request.GET.get('rooms')
    price_min = request.GET.get('priceMin')
    price_max = request.GET.get('priceMax')
    floor = request.GET.get('floor')
    complex_name = request.GET.get('complex')

    if rooms:
        if rooms == "3":  # 3+
            flats = flats.filter(flat_type__gte=3)
        else:
            flats = flats.filter(flat_type=rooms)

    if price_min:
        flats = flats.filter(price__gte=price_min)

    if price_max:
        flats = flats.filter(price__lte=price_max)

    if floor:
        if floor == "2-5":
            flats = flats.filter(floor__gte=2, floor__lte=5)
        elif floor == "6+":
            flats = flats.filter(floor__gte=6)
        else:
            flats = flats.filter(floor=floor)

    if complex_name:
        flats = flats.filter(complex=complex_name)

    if order == 'desc':
        flats = flats.order_by(f'-{sort}')
    else:
        flats = flats.order_by(sort)

    complexes = Flat.objects.values_list("complex", flat=True).distinct()

    page_number = request.GET.get('page', 1)
    paginator = Paginator(flats, 6)
    page_obj = paginator.get_page(page_number)

    querydict = request.GET.copy()
    if 'page' in querydict:
        querydict.pop('page')

    user_agent = request.META.get("HTTP_USER_AGENT", "").lower()
    if "mobile" in user_agent:
        return render(request, "main/mobile_flat.html", {
            'page_obj': page_obj,
            'sort': sort,
            'flats': flats,
            'complexes': complexes,
            'order': order,
            'query_params': querydict.urlencode(),
        })
    else:
        return render(request, "main/flat.html", {
            'page_obj': page_obj,
            'sort': sort,
            'flats': flats,
            'complexes': complexes,
            'order': order,
            'query_params': querydict.urlencode(),
        })
@login_required
def info(request):
    return render(request, "main/info.html")
@login_required
def application(request):
    error = ""
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("application")
        else:
            error = "Хуита"

    form = ApplicationForm()
    data = {
        "form": form,
        "error": error
    }
    return render(request, "main/application.html", data)
@login_required
def filter(request):
    return render(request, "main/filter.html")

@login_required
def home(request):
    return render(request, 'main/default.html')

def register(request):
    login_form = AuthenticationForm(request, data=request.POST or None)
    register_form = RegisterForm()

    if request.method == 'POST':
        # Проверяем, отправлен ли логин
        if 'login_submit' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('/')  # редирект после входа

        # Проверяем, отправлена ли регистрация
        elif 'register_submit' in request.POST:
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                return redirect('/')

    return render(request, 'registration/login.html', {
        'form': login_form,
        'register_form': register_form,
    })


def logout_view(request):
    logout(request)
    return redirect('/')


def process_xml(request):
    if request.method != "POST":
        return JsonResponse({"error": "Только POST-запросы"}, status=405)
    try:
        data = json.loads(request.body)
        url = data.get("url")
        file_id = data.get("file_id")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Неверный JSON"}, status=400)
    if not url or not file_id:
        return JsonResponse({"error": "url и file_id обязательны"}, status=400)
    tag = {
        "flat_id": ["internal-id"],
        "number": ["number"],
        "complex": ["object", "name"],
        "complex_id": ["object", "id"],
        "house": ["house", "name"],
        "house_id": ["house", "id"],
        "type_room": ["property_type"],
        "floor": ["floor"],
        "section": ["building-section"],
        "rooms": ["rooms"],
        "price": ["price", "value"],
        "price_base": ["price", "value"],
        "area": ["area", "value"],
        "areaH": ["living-space", "value"],
        "areaK": ["kitchen-space", "value"],
        "status": ["status-humanized"],
        "plan": ["image"],
        "floor_plan": ["image"]
    }
    file_id, ok = xml_load(url, file_id, **tag)
    return JsonResponse({"file_id": file_id, "ok": ok})