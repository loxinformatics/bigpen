# from django import forms
# from .models import Item


# class OrderForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.items = Item.objects.all()  # Store queryset for validation later
#         for item in self.items:
#             self.fields[f"item_{item.id}"] = forms.IntegerField(
#                 label=f"{item.name} (In Stock: {item.quantity})",
#                 min_value=0,
#                 initial=0,
#                 required=False,
#             )

#     def clean(self):
#         cleaned_data = super().clean()
#         for item in self.items:
#             field_name = f"item_{item.id}"
#             quantity = cleaned_data.get(field_name)
#             if quantity and quantity > item.quantity:
#                 self.add_error(
#                     field_name,
#                     f"Only {item.quantity} left in stock for '{item.name}'.",
#                 )
#         return cleaned_data
