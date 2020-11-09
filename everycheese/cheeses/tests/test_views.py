import pytest
from pytest_django.asserts import assertContains

from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory

from everycheese.users.models import User
from ..models import Cheese
from ..views import (
    CheeseCreateView,
    CheeseListView,
    CheeseDetailView
)
from .factories import CheeseFactory

pytestmark = pytest.mark.django_db

def test_good_cheese_list_view_expanded(rf):
    # Определите URL
    url = reverse("cheeses:list")
    # rf - это ярлык pytest для django.test.RequestFactory
    # Мы генерируем запрос как будто от пользователя, обращающегося
    # к просмотру списка сыров
    request = rf.get(url)
    # Call as_view() сделать вызываемый объект
    # callable_obj аналогичен function-based view
    callable_obj = CheeseListView.as_view()
    # Передайте запрос в callable_obj, чтобы получить
    # HTTP-ответ, обслуживаемый Django
    response = callable_obj(request)
    # Убедитесь, что в ответе HTTP есть 'Cheese List' в
    # HTML и имеет код ответа 200
    assertContains(response, 'Список сыров')

def test_good_cheese_list_view(rf):
    # Получите самое лучшее
    request = rf.get(reverse("cheeses:list"))
    # Используйте запрос, чтобы получить ответ
    response = CheeseListView.as_view()(request)
    # Проверьте правильность ответа
    assertContains(response, 'Список сыров')

def test_good_cheese_detail_view(rf):
    # Закажите сыр на CheeseFactoryy
    cheese = CheeseFactory()
    # Сделайте заявку на наш новый сыр
    url = reverse("cheeses:detail", kwargs={'slug': cheese.slug})
    request = rf.get(url)
    # Используйте запрос, чтобы получить ответ
    callable_obj = CheeseDetailView.as_view()
    response = callable_obj(request, slug=cheese.slug)
    # Проверьте правильность ответа
    assertContains(response, cheese.name)

def test_good_cheese_create_view(rf, admin_user):
    # Закажите сыр на CheeseFactory
    cheese = CheeseFactory()
    # Сделайте заявку на наш новый сыр
    request = rf.get(reverse("cheeses:add"))
    # Добавить аутентифицированного пользователя
    request.user = admin_user
    # Используйте запрос, чтобы получить ответ
    response = CheeseCreateView.as_view()(request)
    # Проверьте правильность ответа
    assert response.status_code == 200

def test_cheese_list_contains_2_cheeses(rf):
    # Создадим парочку сыров
    cheese1 = CheeseFactory()
    cheese2 = CheeseFactory()
    # Создайте запрос, а затем ответ
    # для списка сыров
    request = rf.get(reverse('cheeses:list'))
    response = CheeseListView.as_view()(request)
    # Утвердите, что ответ содержит оба названия сыра
    # в шаблоне.
    assertContains(response, cheese1.name)
    assertContains(response, cheese2.name)

def test_detail_contains_cheese_data(rf):
    cheese = CheeseFactory()
    # Сделайте заявку на наш новый сыр
    url = reverse("cheeses:detail", kwargs={'slug': cheese.slug})
    request = rf.get(url)
    # Используйте запрос, чтобы получить ответ
    callable_obj = CheeseDetailView.as_view()
    response = callable_obj(request, slug=cheese.slug)
    # Давайте проверим наши «Веселые» детали!
    assertContains(response, cheese.name)
    assertContains(response, cheese.get_firmness_display())
    assertContains(response, cheese.country_of_origin.name)

def test_cheese_create_form_valid(rf, admin_user):
    # Submit the cheese add form
    form_data = {
        "name": "Paski Sir",
        "description": "Соленый твердый сыр",
        "firmness": Cheese.Firmness.HARD
    }
    request = rf.post(reverse("cheeses:add"), form_data)
    request.user = admin_user
    response = CheeseCreateView.as_view()(request)
    # Получите сыр по названию
    cheese = Cheese.objects.get(name="Paski Sir")
    # Убедитесь, что сыр соответствует нашей форме
    assert cheese.description == "Соленый твердый сыр"
    assert cheese.firmness == Cheese.Firmness.HARD
    assert cheese.creator == admin_user
