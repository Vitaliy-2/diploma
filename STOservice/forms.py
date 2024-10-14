from django import forms
from .models import Visit
import re


class VisitModelForm(forms.ModelForm):
    # Служебный класс только для параметров. Изолирует переменные, чтобы джанго брал их тут.
    class Meta:
        # Ссылка на конкретную модель, с которой связанна форма
        model = Visit
        # Поля из модели, которые будут отображаться
        fields = ['name', 'phone', 'vin', 'comment', 'section', 'services']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Имя', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'type': 'tel', 'placeholder': 'Номер телефона', 'class': 'form-control'}),
            'vin': forms.TextInput(attrs={'placeholder': 'Vin автомобиля (желательно)', 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Комментарий', 'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'services': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если форма содержит ошибки, добавляем класс 'is-invalid' к соответствующим полям
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                widget_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f'{widget_classes} is-invalid'


    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()

        # Проверяем формат номера телефона: либо +7..., либо 8...
        phone_pattern = r'^(\+7|8)\d{10}$'
        if not re.match(phone_pattern, phone):
            raise forms.ValidationError('Номер телефона должен начинаться с +7 или с 8 и содержать 10 цифр после кода страны.')

        return phone
    
    def clean_name(self):
        name = self.cleaned_data["name"]
        
        if not isinstance(name, str):
            # Поднимаем исключение, которое попадет в контекст шаблона
            raise forms.ValidationError("Имя должно быть строкой")
        return name
    
    # def clean_vin(self):
    #     vin = self.cleaned_data["vin"]
        
    #     if not (vin.lenght == 17) or not (''):
    #         # Поднимаем исключение, которое попадет в контекст шаблона
    #         raise forms.ValidationError("Vin должен содержать 17 символом или быть пустым")
    #     return vin


# Расширяем исходну форму для дополнительного поля status (для администрации)
class VisitEditModelForm(VisitModelForm):
    class Meta(VisitModelForm.Meta):
        fields = VisitModelForm.Meta.fields + ["status"]
        widgets = {
            **VisitModelForm.Meta.widgets,
            "status": forms.Select(attrs={"class": "form-control"}),
        }
