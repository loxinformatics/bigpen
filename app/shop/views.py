from django.shortcuts import render, get_object_or_404

from .models import Category, Item


def ShopDashboard(request):
    category_name = request.GET.get("category", "")

    if category_name:
        items = Item.objects.filter(category__name=category_name)
    else:
        items = Item.objects.all()

    extra_context = {
        "page_title": [
            {
                "label": "All Categories",
                "url": "/shop" if category_name else None,
            }
        ]
        + ([{"label": category_name, "url": None}] if category_name else []),
        "has_header": True,
        "header_has_breadcrumbs": True,
        "has_footer": True,
        "categories": Category.objects.all(),
        "items": items,
        "category_param": category_name,
    }

    return render(request, "shop/categories.html", extra_context)


def ItemDetailView(request, pk):
    item = get_object_or_404(Item, pk=pk)
    images = item.otherImages.all()

    context = {
        "item": item,
        "images": images,
        "page_title": [{"label": item.name, "url": None}],
        "has_header": True,
        "has_footer": True,
    }
    return render(request, "shop/item_detail.html", context)