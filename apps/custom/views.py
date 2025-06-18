from django.views.generic import TemplateView


class Dashboard(TemplateView):
    template_name = "custom/index.html"
    extra_context = {"page_title": "Dashboard"}


class ContactView(TemplateView):
    template_name = "custom/index.html"
    extra_context = {
        "page_title": "Contact",
        "show_contact": True,
    }


# def ShopDashboard(request):
#     category_name = request.GET.get("category", "")

#     if category_name:
#         items = Item.objects.filter(category__name=category_name)
#     else:
#         items = Item.objects.all()

#     extra_context = {
#         "page_title": [
#             {
#                 "label": "All Categories",
#                 "url": "/shop/items" if category_name else None,
#             }
#         ]
#         + ([{"label": category_name, "url": None}] if category_name else []),
#         "has_header": True,
#         "has_footer": True,
#         "categories": Category.objects.all(),
#         "items": items,
#         "category_param": category_name,
#     }

#     return render(request, "shop/categories.html", extra_context)


# def ItemDetailView(request, pk):
#     item = get_object_or_404(Item, pk=pk)
#     images = item.otherImages.all()

#     context = {
#         "item": item,
#         "images": images,
#         "page_title": [
#             {
#                 "label": "All Categories",
#                 "url": "/shop/items",
#             },
#             {
#                 "label": item.category.name,
#                 "url": f"/shop/items/?category={item.category.name}",
#             },
#             {"label": item.name, "url": None},
#         ],
#         "has_header": True,
#         "has_footer": True,
#     }
#     return render(request, "shop/item_detail.html", context)


# @login_required
# def place_order(request):
#     if request.method == "POST":
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = Order.objects.create(user=request.user)
#             for item in Item.objects.all():
#                 quantity = form.cleaned_data.get(f"item_{item.id}")
#                 if quantity and quantity > 0:
#                     OrderItem.objects.create(order=order, item=item, quantity=quantity)
#                     # Subtract from stock
#                     item.quantity -= quantity
#                     item.save()
#             return redirect("order_success")  # Make sure this exists
#     else:
#         form = OrderForm()

#     return render(request, "shop/place_order.html", {"form": form})
