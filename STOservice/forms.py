from django import forms
from .models import Visit, Review
import re


class VisitModelForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['name', 'phone', 'brand', 'number_plate', 'comment', 'section', 'services']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Имя', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'type': 'tel', 'placeholder': 'Номер телефона', 'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'placeholder': 'Марка автомобиля', 'class': 'form-control'}),
            'number_plate': forms.TextInput(attrs={'placeholder': 'Номер автомобиля', 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Комментарий', 'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'services': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['section'].empty_label = "Выберите раздел"
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


# Расширяем исходну форму для дополнительного поля status (для администрации)
class VisitEditModelForm(VisitModelForm):
    class Meta(VisitModelForm.Meta):
        fields = VisitModelForm.Meta.fields + ["status"]
        widgets = {
            **VisitModelForm.Meta.widgets,
            "status": forms.Select(attrs={"class": "form-control"}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ваш отзыв'}),
        }