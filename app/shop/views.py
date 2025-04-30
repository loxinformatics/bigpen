from django.shortcuts import render


def ShopDashboard(request):
    extra_context = {
        "has_header": True,
        "has_footer": True,
    }
    return render(request, "shop/page.html", extra_context)
