from django import forms

from mainapp.models import Product
from ordersapp.models import Order, OrderItem


class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class OrderForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ('user',)
        #exclude = ('user', 'is_active', 'status')


class OrderItemForm(FormControlMixin, forms.ModelForm):
    price = forms.CharField(label='цена', required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # оптимизация запроса на получение имен категорий, теперь в 
        # сете запросов для каждой формы не будут дублироваться запросы на получение имен категорий для каждой формы
        self.fields['product'].queryset = Product.get_items()

    class Meta:
        model = OrderItem
        fields = '__all__'
        # exclude = ()
