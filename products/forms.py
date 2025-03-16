from django import forms

class ProductImportForm(forms.Form):
    file = forms.FileField(label="Выберите CSV файл", help_text="Файл должен содержать: name, description, price, stock, category_name")
