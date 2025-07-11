from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models.stock import Category, Item
from ..serializers.stock import (
    CategoryDetailSerializer,
    CategoryListSerializer,
    ItemListSerializer,
)


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["is_active"]  # Allows usage of ?is_active=true
    search_fields = ["name"]  # Allows usage of ?search=name

    def get_serializer_class(self):
        """
        Return different serializers for different actions.

        Actions and their corresponding HTTP methods:
        - list: GET /categories/ - List all categories
        - retrieve: GET /categories/{id}/ - Get specific category
        """
        if self.action == "list":
            return CategoryListSerializer
        elif self.action == "retrieve":
            return CategoryDetailSerializer
        return CategoryListSerializer  # Default fallback

    @action(detail=True, methods=["get"])
    def items(self, request, pk=None):
        """
        Custom action to return all active items in this category.

        - GET /categories/{id}/items/
        """
        category = self.get_object()
        items = category.items.filter(is_active=True)
        serializer = ItemListSerializer(items, many=True, context={"request": request})
        return Response(serializer.data)


class ItemDetailView(View):
    def get(self, request, id):
        item = get_object_or_404(Item, pk=id)
        extra_context = {"item": item}

        html = render_to_string("ecommerce/swaps/item.html", extra_context)
        return HttpResponse(html)


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
