import django.forms as forms

from app.models import *

class ClientForm(forms.Form):
    name = forms.CharField(max_length = 100, error_messages = {
        "required": "Необходимо ввести имя",
        "max_length": "Имя слишком длинное"
    })
    surname = forms.CharField(max_length = 100, error_messages = {
        "required": "Необходимо ввести фамилию",
        "max_length": "Фамилия слишком длинная"
    })
    otch = forms.CharField(max_length = 100, required = False, error_messages = {
        "max_length": "Отчество слишком длинное"
    })
    phone = forms.CharField(max_length = 50, error_messages = {
        "required": "Необходимо ввести номер телефона",
        "max_length": "Номер телефона слишком длинный"
    })


class ClientOrderForm(forms.Form):
    comment = forms.CharField(max_length = 200, required = False, error_messages = {
        "max_length": "Комментарий слишком длинный"
    })


class FoodForm(forms.Form):
    name = forms.CharField(max_length = 100, error_messages = {
        "required": "Необходимо ввести наименование блюда",
        "max_length": "Наименование блюда слишком длинное"
    })
    price = forms.DecimalField(max_value = 1000000, min_value = 0, decimal_places = 2, error_messages = {
        "required": "Необходимо ввести стоимость блюда",
        "invalid": "Неверно введена стоимость блюда",
        "min_value": "Стоимость блюда не может быть отрицательной",
        "max_value": "Стоимость блюда слишком большая"
    })
    portionsize = forms.IntegerField(min_value = 1, error_messages = {
        "required": "Необходимо ввести размер порции",
        "invalid": "Неверно введён размер порции",
        "min_value": "Размер порции должен быть равен 1 или больше",
    })
    description = forms.CharField(max_length = 500, required = False, error_messages = {
        "max_length": "Слишком длинное описание"
    })
    measureid = forms.ModelChoiceField(queryset = Measure.objects.all(), required = False, error_messages = {
        "invalid": "Неверно введена единица измерения",
    })


class AddOrderedFoodForm(forms.Form):
    foodid = forms.ModelChoiceField(queryset = Food.objects.all())
    count = forms.IntegerField(min_value = 1)


class SearchForm(forms.Form):
    search = forms.CharField(max_length = 200, min_length = 1)


class MeasureForm(forms.Form):
    name = forms.CharField(max_length = 10)